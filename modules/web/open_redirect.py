#!/usr/bin/env python3
"""
Open Redirect Scanner - COMPLETE FIX
Handles HTTP/HTTPS correctly with proper parameter encoding
"""

import requests
import urllib.parse
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class OpenRedirectScanner:
    """Fixed open redirect scanner - No more concatenation errors!"""
    
    def __init__(self, url):
        # Store original
        self.original_url = url
        
        # CRITICAL FIX: Extract just the base domain with proper protocol
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Parse the URL properly
        parsed = urllib.parse.urlparse(url)
        self.scheme = parsed.scheme
        self.netloc = parsed.netloc
        self.base_url = f"{self.scheme}://{self.netloc}"
        self.path = parsed.path if parsed.path else ''
        
        print(f"[*] Open redirect scanner initialized for: {self.base_url}")
        
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.verify = False
        self.session.allow_redirects = False
        self.session.timeout = 3
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (AION Security Scanner)'
        })
        
    def scan(self):
        """Scan for open redirect vulnerabilities"""
        print("[*] Scanning for open redirect vulnerabilities...")
        
        # First, check if site is reachable
        if not self._is_site_reachable():
            print("[*] Site unreachable - skipping open redirect scan")
            return []
        
        # Common redirect parameters to test
        redirect_params = [
            'redirect', 'url', 'next', 'return', 'goto', 'target', 
            'dest', 'destination', 'out', 'view', 'redir', 'continue',
            'return_to', 'return_url', 'redirect_uri', 'redirect_to',
            'r', 'u', 'link', 'go', 'to', 'file', 'document', 'path'
        ]
        
        # Test payloads with different protocols
        payloads = [
            'https://google.com',
            'http://google.com',
            '//google.com',
            'https://evil.com',
            'http://evil.com',
            '//evil.com',
            'https://bing.com',
            'http://bing.com',
            'https://example.com',
            'http://example.com'
        ]
        
        found_count = 0
        tested_count = 0
        
        for param in redirect_params:
            if found_count >= 3:  # Stop after finding 3 vulns
                break
                
            for payload in payloads:
                try:
                    # CRITICAL FIX: Build URL properly with parameters
                    # NEVER concatenate URLs directly!
                    encoded_payload = urllib.parse.quote(payload, safe='')
                    
                    # Method 1: Simple parameter append (works for most sites)
                    test_url = f"{self.base_url}{self.path}?{param}={encoded_payload}"
                    
                    tested_count += 1
                    if tested_count % 10 == 0:
                        print(f"[*] Tested {tested_count} combinations...")
                    
                    # Send request
                    response = self.session.get(test_url, timeout=2)
                    
                    # Check for redirect status codes
                    if response.status_code in [301, 302, 303, 307, 308]:
                        location = response.headers.get('Location', '')
                        
                        # Check if redirect goes to external site
                        if any(domain in location.lower() for domain in ['google.com', 'evil.com', 'bing.com', 'example.com']):
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
                            break  # Break payload loop if found
                            
                except requests.exceptions.ConnectionError:
                    # Connection refused - site may be blocking or parameter doesn't exist
                    continue
                except requests.exceptions.Timeout:
                    continue
                except Exception:
                    continue
        
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
