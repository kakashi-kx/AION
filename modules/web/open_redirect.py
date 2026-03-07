#!/usr/bin/env python3
"""
Open Redirect Scanner - COMPLETELY FIXED VERSION
No more URL concatenation errors!
"""

import requests
import urllib.parse

class OpenRedirectScanner:
    """Bulletproof open redirect scanner"""
    
    def __init__(self, url):
        # Clean the URL - extract just the base
        if url.startswith(('http://', 'https://')):
            self.base_url = url.rstrip('/')
        else:
            self.base_url = 'http://' + url.rstrip('/')
        
        # Extract domain for logging
        parsed = urllib.parse.urlparse(self.base_url)
        self.domain = parsed.netloc
        self.scheme = parsed.scheme
        
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.allow_redirects = False
        self.session.timeout = 3
        
    def scan(self):
        """Scan for open redirect vulnerabilities"""
        print("[*] Scanning for open redirect vulnerabilities...")
        
        # Common redirect parameters
        params = ['redirect', 'url', 'next', 'return', 'goto', 'target']
        
        # Safe test payload
        payload = 'https://example.com'
        encoded_payload = urllib.parse.quote(payload)
        
        found = False
        
        for param in params:
            # CORRECT URL CONSTRUCTION - using parameters
            test_url = f"{self.base_url}/?{param}={encoded_payload}"
            
            try:
                print(f"[*] Testing: {param}")
                response = self.session.get(test_url, timeout=2)
                
                if response.status_code in [301, 302, 303]:
                    location = response.headers.get('Location', '')
                    if 'example.com' in location:
                        vuln = {
                            'type': 'Open Redirect',
                            'url': test_url,
                            'parameter': param,
                            'severity': 'Medium'
                        }
                        self.vulnerabilities.append(vuln)
                        print(f"[!] Open redirect found with parameter: {param}")
                        found = True
                        break
                        
            except requests.exceptions.ConnectionError:
                # Connection refused - normal if no vuln
                continue
            except Exception:
                continue
        
        if not found:
            print("[*] No open redirect vulnerabilities detected")
        else:
            print(f"[+] Found {len(self.vulnerabilities)} open redirect vulnerabilities")
        
        return self.vulnerabilities
