#!/usr/bin/env python3
"""
Open Redirect Scanner - FIXED VERSION
"""

import requests
import urllib.parse

class OpenRedirectScanner:
    """Fixed open redirect scanner"""
    
    def __init__(self, url):
        # Ensure URL has proper protocol
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
        
        # Common redirect parameters to test
        redirect_params = [
            'redirect',
            'url',
            'next',
            'return',
            'return_to',
            'returnurl',
            'return_url',
            'goto',
            'forward',
            'forward_to',
            'target',
            'dest',
            'destination',
            'out',
            'view',
            'dir',
            'redirect_to',
            'redirect_url',
            'redir',
            'redirect_uri',
            'continue',
            'return_path',
            'return_path',
            'r',
            'u'
        ]
        
        # Test payloads
        payloads = [
            'https://google.com',
            'http://google.com',
            '//google.com',
            'https://evil.com',
            'http://evil.com',
            '//evil.com',
            '/\\google.com',
            'https:/google.com',
            'http:/google.com'
        ]
        
        # Test different injection points
        test_paths = [
            f"{self.base_url}/?{{param}}={{payload}}",
            f"{self.base_url}/index.php?{{param}}={{payload}}",
            f"{self.base_url}/redirect.php?{{param}}={{payload}}",
            f"{self.base_url}/go.php?{{param}}={{payload}}",
            f"{self.base_url}/out.php?{{param}}={{payload}}"
        ]
        
        for param in redirect_params:
            for payload in payloads:
                for path_template in test_paths:
                    try:
                        # Build the test URL properly
                        encoded_payload = urllib.parse.quote(payload)
                        test_url = path_template.replace('{param}', param).replace('{payload}', encoded_payload)
                        
                        print(f"[*] Testing: {test_url[:80]}...")
                        
                        # Send request
                        response = self.session.get(test_url)
                        
                        # Check for redirect
                        if response.status_code in [301, 302, 303, 307, 308]:
                            location = response.headers.get('Location', '')
                            
                            # Check if redirect goes to external site
                            if any(domain in location.lower() for domain in ['google.com', 'evil.com']):
                                vuln = {
                                    'type': 'Open Redirect',
                                    'url': test_url,
                                    'parameter': param,
                                    'payload': payload,
                                    'redirects_to': location,
                                    'severity': 'Medium'
                                }
                                self.vulnerabilities.append(vuln)
                                print(f"[!] Open redirect found! Parameter: {param}")
                                
                    except requests.exceptions.ConnectionError as e:
                        # Skip connection errors - they're not vulnerabilities
                        continue
                    except Exception as e:
                        continue
        
        if not self.vulnerabilities:
            print("[*] No open redirect vulnerabilities detected")
        else:
            print(f"[+] Found {len(self.vulnerabilities)} open redirect vulnerabilities")
        
        return self.vulnerabilities
