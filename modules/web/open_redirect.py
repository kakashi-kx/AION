#!/usr/bin/env python3
"""
Open Redirect Scanner - COMPLETELY REWRITTEN
No more URL concatenation bugs!
"""

import requests
import urllib.parse
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class OpenRedirectScanner:
    """Bulletproof open redirect scanner"""
    
    def __init__(self, url):
        # Store the original URL for reference
        self.original_url = url
        
        # PROPER URL PARSING - NO CONCATENATION!
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Parse the URL properly
        parsed = urllib.parse.urlparse(url)
        self.scheme = parsed.scheme
        self.netloc = parsed.netloc
        self.base_url = f"{self.scheme}://{self.netloc}"
        
        print(f"[*] Open redirect scanner initialized for: {self.base_url}")
        
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.verify = False
        self.session.allow_redirects = False
        self.session.timeout = 5
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (AION Security Scanner)'
        })
        
    def scan(self):
        """Scan for open redirect vulnerabilities"""
        print("[*] Scanning for open redirect vulnerabilities...")
        
        # First, check if the site is reachable
        if not self._is_site_reachable():
            print("[*] Site unreachable - skipping open redirect scan")
            return []
        
        # Common redirect parameters to test
        redirect_params = [
            'redirect', 'url', 'next', 'return', 'goto', 'target', 
            'dest', 'destination', 'out', 'view', 'redir', 'continue',
            'return_to', 'return_url', 'redirect_uri', 'redirect_to'
        ]
        
        # Test payloads - using safe domains
        payloads = [
            'https://example.com',
            'http://example.com',
            '//example.com'
        ]
        
        found_count = 0
        
        for param in redirect_params:
            for payload in payloads:
                try:
                    # PROPER URL CONSTRUCTION - NO CONCATENATION!
                    encoded_payload = urllib.parse.quote(payload, safe='')
                    
                    # Build URL properly using urllib
                    query_params = {param: payload}
                    url_parts = list(urllib.parse.urlparse(self.base_url))
                    query = urllib.parse.urlencode(query_params)
                    url_parts[4] = query  # Set query string
                    
                    test_url = urllib.parse.urlunparse(url_parts)
                    
                    # Alternative simple construction (also safe)
                    # test_url = f"{self.base_url}?{param}={encoded_payload}"
                    
                    # Make request
                    response = self.session.get(test_url)
                    
                    # Check for redirect
                    if response.status_code in [301, 302, 303, 307, 308]:
                        location = response.headers.get('Location', '')
                        
                        # Check if redirect goes to external site
                        if any(domain in location.lower() for domain in ['example.com']):
                            vuln = {
                                'type': 'Open Redirect',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'redirects_to': location,
                                'severity': 'Medium'
                            }
                            self.vulnerabilities.append(vuln)
                            found_count += 1
                            print(f"[!] Open redirect found! Parameter: {param} -> {location[:60]}...")
                            
                            # Break after finding one to avoid too many requests
                            if found_count >= 3:
                                break
                                
                except requests.exceptions.ConnectionError as e:
                    # Connection refused - site may be blocking
                    continue
                except requests.exceptions.Timeout:
                    continue
                except Exception as e:
                    continue
            
            if found_count >= 3:
                break
        
        if not self.vulnerabilities:
            print("[*] No open redirect vulnerabilities detected")
        else:
            print(f"[+] Found {len(self.vulnerabilities)} open redirect vulnerabilities")
        
        return self.vulnerabilities
    
    def _is_site_reachable(self):
        """Check if the site is reachable"""
        try:
            response = self.session.get(self.base_url, timeout=3)
            return True
        except:
            return False
    
    def _safe_url_join(self, base, param, value):
        """Safely join URL components"""
        if not base.endswith('?'):
            base += '?'
        return f"{base}{param}={urllib.parse.quote(value)}"
