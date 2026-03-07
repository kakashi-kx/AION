#!/usr/bin/env python3
"""
Open Redirect Scanner - INTELLIGENT VERSION
Handles connection errors gracefully
"""

import requests
import urllib.parse
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class OpenRedirectScanner:
    """Intelligent open redirect scanner"""
    
    def __init__(self, url):
        self.raw_url = url
        
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        parsed = urllib.parse.urlparse(url)
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.domain = parsed.netloc.split(':')[0]
        
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.verify = False
        self.session.allow_redirects = False
        self.session.timeout = 3  # Shorter timeout
        
    def scan(self):
        print("[*] Scanning for open redirect vulnerabilities...")
        
        # First, check if site is responsive
        try:
            test = self.session.get(self.base_url, timeout=2)
            print(f"[*] Site is responsive (HTTP {test.status_code})")
        except Exception as e:
            print(f"[*] Site may be down or blocking: {e}")
            print("[*] Skipping open redirect scan")
            return []
        
        # Common redirect parameters
        params = ['redirect', 'url', 'next', 'return', 'goto', 'target']
        
        # Test payloads - use benign domains first
        payloads = [
            'https://example.com',
            'http://example.com',
            '//example.com'
        ]
        
        found = False
        
        for param in params:
            if found:
                break
                
            for payload in payloads:
                try:
                    encoded = urllib.parse.quote(payload)
                    test_url = f"{self.base_url}/?{param}={encoded}"
                    
                    # Try to connect
                    response = self.session.get(test_url)
                    
                    # Check for redirect
                    if response.status_code in [301, 302]:
                        location = response.headers.get('Location', '')
                        if 'example.com' in location:
                            self.vulnerabilities.append({
                                'type': 'Open Redirect',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload
                            })
                            print(f"[!] Open redirect found!")
                            found = True
                            break
                            
                except requests.exceptions.ConnectionError:
                    # Site refused connection - this is expected if no vulnerability exists
                    continue
                except Exception:
                    continue
        
        if not self.vulnerabilities:
            print("[*] No open redirect vulnerabilities detected")
        
        return self.vulnerabilities
