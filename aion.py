
#!/usr/bin/env python3
"""
AION - Advanced Intrusion Offensive Network
Main CLI Entry Point
Developed by kakashi-kx

MITRE ATT&CK aligned penetration testing framework 
"""

import argparse
import sys
import os
from datetime import datetime
from colorama import init, Fore, Style

# Import modules
from modules.reconnaissance import *
from modules.network import *
from modules.web import *
from modules.exploitation import *
from modules.post_exploitation import *
from modules.crypto import *
from modules.cloud import *
from modules.api import *
from modules.reporting import *
from core.reporter import ReportGenerator

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   {Fore.MAGENTA}█████╗ ██╗ ██████╗ ███╗   ██╗{Fore.CYAN}                                  ║
║   {Fore.MAGENTA}██╔══██╗██║██╔═══██╗████╗  ██║{Fore.CYAN}                                  ║
║   {Fore.MAGENTA}██████╔╝██║██║   ██║██╔██╗ ██║{Fore.CYAN}                                  ║
║   {Fore.MAGENTA}██╔══██╗██║██║   ██║██║╚██╗██║{Fore.CYAN}                                  ║
║   {Fore.MAGENTA}██║  ██║██║╚██████╔╝██║ ╚████║{Fore.CYAN}                                  ║
║   {Fore.MAGENTA}╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝{Fore.CYAN}                                  ║
║                                                                       ║
║   {Fore.GREEN}Advanced Intrusion Offensive Network v2.0{Fore.CYAN}                        ║
║   {Fore.YELLOW}Developed by kakashi-kx{Fore.CYAN}                                          ║
║                                                                       ║
║   {Fore.WHITE}Features:{Fore.CYAN}                                                           ║
║   • 50+ Security Modules • MITRE ATT&CK Mapping • Professional Reports  ║
║   • Network Recon • Web Vuln Scan • Exploitation • Post-Exploit      ║
║   • Cloud Security • API Testing • Crypto Tools • And more...        ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

def print_banner():
    """Display AION banner"""
    print(BANNER)

def main():
    parser = argparse.ArgumentParser(description='AION - Complete Penetration Testing Framework')
    parser.add_argument('--target', '-t', help='Target IP or domain')
    parser.add_argument('--module', '-m', choices=[
        'recon', 'network', 'web', 'exploit', 'post', 'crypto', 'cloud', 'api', 'all'
    ], default='all', help='Module to run')
    parser.add_argument('--scan-type', choices=[
        'quick', 'full', 'stealth', 'aggressive'
    ], default='quick', help='Scan profile')
    parser.add_argument('--ports', help='Port range (e.g., 1-1000)')
    parser.add_argument('--wordlist', help='Custom wordlist path')
    parser.add_argument('--threads', type=int, default=50, help='Number of threads')
    parser.add_argument('--timeout', type=int, default=3, help='Connection timeout')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--format', choices=['txt', 'html', 'pdf', 'json'], default='html', help='Report format')
    parser.add_argument('--mitre', action='store_true', help='Include MITRE ATT&CK mapping ')
    parser.add_argument('--list-modules', action='store_true', help='List all available modules')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.list_modules:
        list_all_modules()
        sys.exit(0)
    
    if args.interactive:
        start_interactive_mode()
        sys.exit(0)
    
    if not args.target:
        print(f"{Fore.RED}❌ Error: Target required. Use --target or -i for interactive mode{Style.RESET_ALL}")
        sys.exit(1)
    
    # Initialize results dictionary
    results = {
        'target': args.target,
        'timestamp': datetime.now().isoformat(),
        'modules_run': [],
        'findings': {},
        'summary': {}
    }
    
    # Run selected modules
    if args.module in ['recon', 'all']:
        print(f"\n{Fore.CYAN}[*] Running Reconnaissance Module...{Style.RESET_ALL}")
        results['findings']['recon'] = run_recon_modules(args)
        results['modules_run'].append('recon')
    
    if args.module in ['network', 'all']:
        print(f"\n{Fore.CYAN}[*] Running Network Scanning Module...{Style.RESET_ALL}")
        results['findings']['network'] = run_network_modules(args)
        results['modules_run'].append('network')
    
    if args.module in ['web', 'all']:
        print(f"\n{Fore.CYAN}[*] Running Web Security Module...{Style.RESET_ALL}")
        results['findings']['web'] = run_web_modules(args)
        results['modules_run'].append('web')
    
    if args.module in ['exploit', 'all']:
        print(f"\n{Fore.CYAN}[*] Running Exploitation Module...{Style.RESET_ALL}")
        results['findings']['exploit'] = run_exploit_modules(args)
        results['modules_run'].append('exploit')
    
    if args.module in ['crypto', 'all']:
        print(f"\n{Fore.CYAN}[*] Running Cryptography Module...{Style.RESET_ALL}")
        results['findings']['crypto'] = run_crypto_modules(args)
        results['modules_run'].append('crypto')
    
    # Generate report
    if args.output or args.format:
        print(f"\n{Fore.CYAN}[*] Generating {args.format.upper()} report...{Style.RESET_ALL}")
        reporter = ReportGenerator(args.target, results, args.mitre)
        report_file = reporter.generate(args.format, args.output)
        print(f"{Fore.GREEN}✅ Report saved to: {report_file}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}✅ Scan completed successfully!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📊 Summary: Run {len(results['modules_run'])} modules{Style.RESET_ALL}")

def list_all_modules():
    """List all available modules with descriptions"""
    modules = [
        ("🔍 RECONNAISSANCE", [
            ("dns_enum", "DNS enumeration and zone transfer"),
            ("subdomain_finder", "Discover subdomains"),
            ("whois_lookup", "WHOIS information gathering"),
            ("email_harvester", "Extract email addresses"),
            ("metadata_extractor", "Extract metadata from PDF/DOC files"),
            ("shodan_lookup", "Shodan IP intelligence"),
        ]),
        ("🌐 NETWORK", [
            ("port_scanner", "TCP/UDP port scanning"),
            ("service_detector", "Banner grabbing and service detection"),
            ("os_fingerprint", "Operating system fingerprinting"),
            ("packet_sniffer", "Live packet capture "),
            ("arp_spoof_detector", "Detect ARP spoofing attacks"),
            ("mac_address_lookup", "MAC address vendor lookup "),
            ("traceroute", "Network path discovery "),
            ("ping_sweep", "ICMP sweep for host discovery"),
        ]),
        ("💻 WEB", [
            ("sql_injection", "SQL injection scanner "),
            ("xss_scanner", "Cross-site scripting detector"),
            ("directory_bruteforcer", "Directory and file enumeration"),
            ("admin_finder", "Find admin panels"),
            ("wordpress_scanner", "WordPress vulnerability scanner"),
            ("cloudflare_bypass", "Cloudflare IP resolver"),
            ("crawler", "Web spider for link extraction"),
            ("parameter_fuzzer", "Parameter fuzzing for vulnerabilities"),
            ("file_upload_tester", "Test file upload functionality"),
        ]),
        ("💥 EXPLOITATION", [
            ("reverse_shell_generator", "Generate reverse shell payloads"),
            ("cve_scanner", "CVE vulnerability lookup"),
            ("default_creds", "Test default credentials"),
            ("brute_forcer", "Brute force SSH/FTP/MySQL "),
        ]),
        ("🔐 CRYPTO", [
            ("hash_cracker", "MD5/SHA1/SHA256 hash cracking"),
            ("password_analyzer", "Password strength analysis"),
            ("encrypt_decrypt", "File encryption/decryption"),
            ("ssl_scanner", "SSL/TLS security scanning "),
        ]),
        ("☁️ CLOUD", [
            ("aws_scanner", "AWS misconfiguration scanner "),
            ("azure_scanner", "Azure security scanner "),
            ("gcp_scanner", "GCP security scanner "),
        ]),
        ("🔌 API", [
            ("api_fuzzer", "REST API fuzzing "),
            ("graphql_scanner", "GraphQL vulnerability scanner "),
            ("jwt_tester", "JWT token security testing"),
        ]),
    ]
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"📋 AION MODULE CATALOG - 50+ Security Tools")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    for category, tools in modules:
        print(f"{Fore.YELLOW}{category}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*40}{Style.RESET_ALL}")
        for tool, desc in tools:
            print(f"  {Fore.GREEN}►{Style.RESET_ALL} {tool:20} - {desc}")
        print()

def start_interactive_mode():
    """Interactive mode for AION"""
    print(f"\n{Fore.CYAN}[*] Starting interactive mode...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Type 'help' for commands, 'exit' to quit{Style.RESET_ALL}\n")
    
    while True:
        try:
            cmd = input(f"{Fore.GREEN}aion>{Style.RESET_ALL} ").strip()
            
            if cmd == 'exit':
                break
            elif cmd == 'help':
                print_help()
            elif cmd.startswith('scan'):
                # Parse scan command
                parts = cmd.split()
                if len(parts) >= 2:
                    target = parts[1]
                    print(f"Scanning {target}...")
                else:
                    print("Usage: scan <target>")
            elif cmd == 'modules':
                list_all_modules()
            else:
                print(f"Unknown command: {cmd}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

def print_help():
    """Print interactive mode help"""
    help_text = f"""
{Fore.CYAN}Available Commands:{Style.RESET_ALL}
  scan <target>     - Run quick scan on target
  fullscan <target> - Run full scan on target
  modules           - List all modules
  help              - Show this help
  exit              - Exit interactive mode
    """
    print(help_text)

def run_recon_modules(args):
    """Run reconnaissance modules"""
    results = {}
    
    # DNS Enumeration
    from modules.reconnaissance.dns_enum import DNSEnumerator
    dns = DNSEnumerator(args.target)
    results['dns'] = dns.enumerate()
    
    # Subdomain Finder
    from modules.reconnaissance.subdomain_finder import SubdomainFinder
    subfinder = SubdomainFinder(args.target, args.wordlist)
    results['subdomains'] = subfinder.find()
    
    # WHOIS Lookup
    from modules.reconnaissance.whois_lookup import WhoisLookup
    whois = WhoisLookup(args.target)
    results['whois'] = whois.lookup()
    
    return results

def run_network_modules(args):
    """Run network scanning modules"""
    results = {}
    
    # Port Scanner
    from modules.network.port_scanner import PortScanner
    scanner = PortScanner(args.target, args.threads, args.timeout)
    results['ports'] = scanner.scan(args.ports)
    
    # Service Detection
    from modules.network.service_detector import ServiceDetector
    detector = ServiceDetector(args.target)
    results['services'] = detector.detect(results['ports'])
    
    # OS Fingerprinting
    from modules.network.os_fingerprint import OSFingerprinter
    fingerprinter = OSFingerprinter(args.target)
    results['os'] = fingerprinter.fingerprint()
    
    return results

def run_web_modules(args):
    """Run web security modules"""
    results = {}
    
    # SQL Injection Scanner
    from modules.web.sql_injection import SQLInjectionScanner
    sqli = SQLInjectionScanner(args.target, args.threads)
    results['sqli'] = sqli.scan()
    
    # XSS Scanner
    from modules.web.xss_scanner import XSSScanner
    xss = XSSScanner(args.target)
    results['xss'] = xss.scan()
    
    # Directory Bruteforcer
    from modules.web.directory_bruteforcer import DirectoryBruteforcer
    dirb = DirectoryBruteforcer(args.target, args.wordlist)
    results['directories'] = dirb.bruteforce()
    
    return results

def run_exploit_modules(args):
    """Run exploitation modules"""
    results = {}
    
    # CVE Scanner
    from modules.exploitation.cve_scanner import CVEScanner
    cve = CVEScanner(args.target)
    results['cves'] = cve.scan()
    
    # Default Credentials Tester
    from modules.exploitation.default_creds import DefaultCredsTester
    creds = DefaultCredsTester(args.target)
    results['default_creds'] = creds.test()
    
    return results

def run_crypto_modules(args):
    """Run cryptography modules"""
    results = {}
    
    # SSL/TLS Scanner
    from modules.crypto.ssl_scanner import SSLScanner
    ssl = SSLScanner(args.target)
    results['ssl'] = ssl.scan()
    
    return results

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
