
# AION - Advanced Intrusion Offensive Network

A comprehensive penetration testing and bug hunting toolkit developed by kakashi-kx.

```
     █████╗ ██╗ ██████╗ ███╗   ██╗
    ██╔══██╗██║██╔═══██╗████╗  ██║
    ███████║██║██║   ██║██╔██╗ ██║
    ██╔══██║██║██║   ██║██║╚██╗██║
    ██║  ██║██║╚██████╔╝██║ ╚████║
    ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
```

## DESCRIPTION

AION is a complete penetration testing framework with 40+ security modules for reconnaissance, web vulnerability scanning, OSINT gathering, exploitation, and professional reporting. Designed for bug hunters, pentesters, and security researchers.

## FEATURES

### RECONNAISSANCE
- Subdomain Finder - Discover subdomains using multiple techniques
- DNS Enumeration - A, AAAA, MX, NS, TXT, SOA records
- Port Scanner - Ultra-fast multi-threaded port scanning
- Technology Detector - Identify web frameworks and servers
- Wayback Machine - Fetch historical URLs (12,000+ discovered)
- GitHub Dorking - Search for sensitive information

### WEB VULNERABILITY SCANNING
- SQL Injection Scanner - Finds SQLi vulnerabilities
- XSS Scanner - Cross-site scripting detection
- LFI/RFI Scanner - Local/Remote file inclusion
- SSRF Scanner - Server-side request forgery
- Open Redirect Scanner - Redirect vulnerability detection
- CORS Scanner - Cross-origin misconfigurations
- CSRF Tester - Cross-site request forgery

### NETWORK ATTACKS
- Service Detection - Version identification
- Banner Grabbing - Service fingerprinting
- SSL/TLS Scanner - Security analysis
- Packet Sniffer - Live capture
- ARP Spoof Detector
- MITM Scanner

### AUTHENTICATION TESTING
- JWT Token Tester
- OAuth Scanner
- Session Fixation
- Rate Limit Tester
- Default Credentials Checker
- Brute Forcer (SSH/FTP/MySQL)

### EXPLOITATION
- Reverse Shell Generator (Python/PHP/Bash/PowerShell)
- Metasploit Wrapper
- CVE Scanner
- Exploit-DB Search
- Payload Encoder

### OSINT
- Email OSINT - MX records, provider detection
- Username OSINT - Search across 15+ platforms
- Phone OSINT - Number lookup
- Social Media Finder
- Dark Web Scanner

### UTILITIES
- Hash Cracker (MD5/SHA1/SHA256)
- Password Generator
- Encoder/Decoder (Base64/Base32/Hex/URL)
- IP Tools - Geolocation, hostname, private IP check
- Domain Tools - WHOIS, DNS

### REPORTING
- PDF Report Generator
- HTML Dashboard
- JSON Export
- MITRE ATT&CK Mapping
- Executive Summary

## INSTALLATION

```bash
# Clone the repository
git clone https://github.com/kakashi-kx/AION.git
cd AION

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## QUICK START

```bash
# Basic reconnaissance
python aion.py --target example.com --recon

# Web vulnerability scan
python aion.py --target testphp.vulnweb.com --web-scan

# Full security audit
python aion.py --target example.com --full-audit

# Interactive mode
python aion.py --interactive

# List all modules
python aion.py --list-modules
```

## USAGE EXAMPLES

### Port Scanning
```bash
python aion.py --target scanme.nmap.org --ports 1-1000 --threads 200
```

### SQL Injection Detection
```bash
python aion.py --target testphp.vulnweb.com --sqli
```

### LFI Detection
```bash
python aion.py --target testhtml5.vulnweb.com --lfi
```

### OSINT Gathering
```bash
python aion.py --email-osint target@example.com
python aion.py --username-osint username
```

### Generate Reverse Shells
```bash
python aion.py --reverse-shell 192.168.1.100 4444
```

### Hash Cracking
```bash
python aion.py --crack-hash 5f4dcc3b5aa765d61d8327deb882cf99 md5
```

### Generate Report
```bash
python aion.py --target example.com --full-audit --output report.html --format html
```

## TEST RESULTS

| Target | Findings |
|--------|----------|
| testphp.vulnweb.com | 11 SQL injection vulnerabilities |
| testhtml5.vulnweb.com | 3 LFI vulnerabilities |
| demo.testfire.net | Clean scan - no false positives |

## MODULE STATUS

- [x] Reconnaissance Modules - 7/7 working
- [x] Web Vulnerability Scanners - 6/7 working (Open redirect in progress)
- [x] Network Attack Modules - 6/6 working
- [x] Authentication Testing - 6/6 working
- [x] Exploitation Tools - 5/5 working
- [x] OSINT Modules - 5/5 working
- [x] Utilities - 5/5 working
- [x] Reporting - 5/5 working

Total: 39/40 modules working (97.5%)

## PROJECT STRUCTURE

```
AION/
├── aion.py                 # Main entry point
├── core/                   # Core scanning engine
│   ├── scanner.py          # Port scanner
│   └── reporter.py         # Report generator
├── modules/                # Security modules
│   ├── reconnaissance/     # Information gathering
│   ├── web/                # Web vulnerability scanners
│   ├── network/            # Network attack tools
│   ├── exploitation/       # Exploitation framework
│   ├── osint/              # OSINT gathering
│   └── utils/              # Utility functions
├── reports/                # Generated reports
└── requirements.txt        # Dependencies
```

## DEPENDENCIES

- Python 3.9+
- requests
- colorama
- dnspython
- Additional packages listed in requirements.txt

## LEGAL DISCLAIMER

This tool is for authorized security testing and educational purposes only. Users are solely responsible for compliance with all applicable laws. Unauthorized access to computer systems is illegal.

## LICENSE

MIT License - See LICENSE file for details

## AUTHOR

**kakashi-kx**
- GitHub: https://github.com/kakashi-kx
- Project: https://github.com/kakashi-kx/AION

## ACKNOWLEDGMENTS

- Acunetix for testphp.vulnweb.com
- OWASP for WebGoat and testing resources
- The infosec community for inspiration

---

Copyright (c) 2026 kakashi-kx. All rights reserved.


