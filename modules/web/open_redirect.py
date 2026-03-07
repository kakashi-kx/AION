#!/usr/bin/env python3
"""
Open Redirect Scanner - ULTIMATE FIXED VERSION
Works with any target
"""

import requests
import urllib.parse
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class OpenRedirectScanner:
    """Completely fixed open redirect scanner"""
    
    def __init__(self, url):
        # CRITICAL FIX: Properly parse and normalize the URL
        self.raw_url = url
        
        # Remove any trailing slashes and ensure proper format
        if isinstance(url, str):
            url = url.strip()
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Parse the URL to get components
        parsed = urllib.parse.urlparse(url)
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.domain = parsed.netloc.split(':')[0]  # Remove port if present
        
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.verify = False
        self.session.allow_redirects = False
        self.session.timeout = 5
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (AION Security Scanner)'
        })
        
    def scan(self):
        print("[*] Scanning for open redirect vulnerabilities...")
        
        # Common redirect parameters to test
        redirect_params = [
            'redirect', 'url', 'next', 'return', 'goto', 'target', 
            'dest', 'destination', 'out', 'view', 'dir', 'redirect_to',
            'redirect_url', 'redir', 'redirect_uri', 'continue',
            'return_path', 'r', 'u', 'link', 'file', 'document',
            'folder', 'root', 'path', 'continue', 'return_to'
        ]
        
        # Test payloads - use multiple domains
        payloads = [
            'https://google.com',
            'http://google.com',
            '//google.com',
            'https://evil.com',
            'http://evil.com',
            '//evil.com',
            'https://bing.com',
            'http://bing.com',
            '//bing.com',
            '/\\google.com',
            'https:/google.com',
            'http:/google.com',
            'https:google.com',
            'http:google.com'
        ]
        
        # Test different injection points
        test_paths = [
            f"{self.base_url}/{{param}}={{payload}}",
            f"{self.base_url}/?{{param}}={{payload}}",
            f"{self.base_url}/index.php?{{param}}={{payload}}",
            f"{self.base_url}/redirect.php?{{param}}={{payload}}",
            f"{self.base_url}/go.php?{{param}}={{payload}}",
            f"{self.base_url}/out.php?{{param}}={{payload}}",
            f"{self.base_url}/link.php?{{param}}={{payload}}"
        ]
        
        found = False
        
        for param in redirect_params:
            for payload in payloads:
                for path_template in test_paths:
                    try:
                        # CRITICAL FIX: Properly encode the payload
                        encoded_payload = urllib.parse.quote(payload, safe='')
                        
                        # Build the test URL correctly - NO CONCATENATION BUGS
                        test_url = path_template.replace('{param}', param).replace('{payload}', encoded_payload)
                        
                        # Ensure the URL is valid
                        if not test_url.startswith(('http://', 'https://')):
                            test_url = 'http://' + test_url.lstrip('/')
                        
                        # Send request
                        response = self.session.get(test_url)
                        
                        # Check for redirect status codes
                        if response.status_code in [301, 302, 303, 307, 308]:
                            location = response.headers.get('Location', '')
                            
                            # Check if redirect goes to external site
                            if any(domain in location.lower() for domain in ['google.com', 'evil.com', 'bing.com']):
                                vuln = {
                                    'type': 'Open Redirect',
                                    'url': test_url,
                                    'parameter': param,
                                    'payload': payload,
                                    'redirects_to': location,
                                    'severity': 'Medium'
                                }
                                self.vulnerabilities.append(vuln)
                                print(f"[!] Open redirect found! Parameter: {param} -> {location[:50]}...")
                                found = True
                                break
                    
                    except requests.exceptions.ConnectionError:
                        # Skip connection errors - they're not vulnerabilities
                        continue
                    except Exception as e:
                        # Silent fail for other errors
                        continue
                
                if found:
                    break
            if found:
                break
        
        if not self.vulnerabilities:
            print("[*] No open redirect vulnerabilities detected")
        else:
            print(f"[+] Found {len(self.vulnerabilities)} open redirect vulnerabilities")
        
        return self.vulnerabilities
