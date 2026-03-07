#!/usr/bin/env python3
"""
Open Redirect Scanner - FIXED VERSION
"""

import requests
import urllib.parse

class OpenRedirectScanner:
    """Fixed open redirect scanner"""
    
    def __init__(self, url):
        # Ensure URL has proper protocol and no trailing slash
        if not url.startswith(('http://', 'https://')):
            self.base_url = 'http://' + url.rstrip('/')
        else:
            self.base_url = url.rstrip('/')
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.verify = False
        self.session.allow_redirects = False
        self.session.timeout = 5
        
    def scan(self):
        print("[*] Scanning for open redirect vulnerabilities...")
        
        # Common redirect parameters
        params = ['redirect', 'url', 'next', 'return', 'goto', 'target', 'dest']
        
        # Test payloads
        payloads = ['https://google.com', 'http://google.com', '//google.com']
        
        for param in params:
            for payload in payloads:
                try:
                    # Build URL correctly - DON'T concatenate
                    encoded = urllib.parse.quote(payload)
                    test_url = f"{self.base_url}/?{param}={encoded}"
                    
                    response = self.session.get(test_url)
                    
                    if response.status_code in [301, 302]:
                        location = response.headers.get('Location', '')
                        if 'google.com' in location:
                            self.vulnerabilities.append({
                                'type': 'Open Redirect',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload
                            })
                            print(f"[!] Open redirect found with parameter: {param}")
                            
                except Exception as e:
                    continue
        
        if not self.vulnerabilities:
            print("[*] No open redirect vulnerabilities detected")
        
        return self.vulnerabilities
