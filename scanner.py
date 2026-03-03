
"""
Advanced Port Scanner Module
Supports TCP, UDP, SYN stealth scans with service detection
Developed by kakashi-kx
Based on industry-standard scanning techniques 
"""

import socket
import threading
import time
import ipaddress
from queue import Queue
from datetime import datetime
from colorama import Fore, Style
import scapy.all as scapy

class PortScanner:
    """
    Multi-threaded port scanner with multiple scan types
    Features:
    - TCP Connect scan
    - SYN stealth scan (requires root)
    - UDP scan
    - Service version detection
    - OS fingerprinting
    """
    
    def __init__(self, target, threads=100, timeout=2, scan_type='tcp'):
        self.target = self.resolve_target(target)
        self.threads = threads
        self.timeout = timeout
        self.scan_type = scan_type
        self.open_ports = []
        self.queue = Queue()
        self.lock = threading.Lock()
        self.service_versions = {}
        
    def resolve_target(self, target):
        """Resolve hostname to IP"""
        try:
            ipaddress.ip_address(target)
            return target
        except:
            try:
                return socket.gethostbyname(target)
            except:
                raise Exception(f"Cannot resolve {target}")
    
    def tcp_connect_scan(self, port):
        """TCP Connect scan (most reliable, no root required)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                service = self.get_service(port)
                banner = self.grab_banner(port)
                with self.lock:
                    self.open_ports.append({
                        'port': port,
                        'protocol': 'tcp',
                        'state': 'open',
                        'service': service,
                        'banner': banner
                    })
                print(f"  {Fore.GREEN}✅ Port {port}/tcp - {service} OPEN{Style.RESET_ALL}")
                if banner:
                    print(f"     Banner: {banner[:50]}...")
            sock.close()
        except:
            pass
    
    def syn_scan(self, port):
        """SYN stealth scan (requires root) - faster and stealthier"""
        try:
            # Craft SYN packet
            packet = scapy.IP(dst=self.target)/scapy.TCP(dport=port, flags='S')
            response = scapy.sr1(packet, timeout=self.timeout, verbose=0)
            
            if response and response.haslayer(scapy.TCP):
                if response.getlayer(scapy.TCP).flags == 0x12:  # SYN-ACK
                    # Send RST to close connection
                    rst_packet = scapy.IP(dst=self.target)/scapy.TCP(dport=port, flags='R')
                    scapy.send(rst_packet, verbose=0)
                    
                    service = self.get_service(port)
                    with self.lock:
                        self.open_ports.append({
                            'port': port,
                            'protocol': 'tcp',
                            'state': 'open',
                            'service': service
                        })
                    print(f"  {Fore.GREEN}✅ Port {port}/tcp - {service} OPEN (SYN){Style.RESET_ALL}")
        except:
            pass
    
    def udp_scan(self, port):
        """UDP port scan (less reliable, may miss open ports)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            sock.sendto(b'', (self.target, port))
            try:
                data, addr = sock.recvfrom(1024)
                with self.lock:
                    self.open_ports.append({
                        'port': port,
                        'protocol': 'udp',
                        'state': 'open',
                        'service': self.get_service(port, 'udp')
                    })
                print(f"  {Fore.GREEN}✅ Port {port}/udp - OPEN{Style.RESET_ALL}")
            except socket.timeout:
                # No response doesn't mean closed
                pass
            sock.close()
        except:
            pass
    
    def grab_banner(self, port):
        """Banner grabbing for service version detection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((self.target, port))
            
            # Send probe based on common services
            probes = {
                21: b'HELP\r\n',  # FTP
                22: b'',           # SSH (banner sent automatically)
                25: b'EHLO test\r\n',  # SMTP
                80: b'HEAD / HTTP/1.0\r\n\r\n',  # HTTP
                110: b'USER test\r\n',  # POP3
                143: b'a001 LOGIN\r\n',  # IMAP
                443: b'HEAD / HTTP/1.0\r\n\r\n',  # HTTPS
                3306: b'',  # MySQL
            }
            
            if port in probes:
                sock.send(probes[port])
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            return banner
        except:
            return None
    
    def get_service(self, port, protocol='tcp'):
        """Get service name for port"""
        common_ports = {
            21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp',
            53: 'dns', 80: 'http', 110: 'pop3', 111: 'rpcbind',
            135: 'msrpc', 139: 'netbios-ssn', 143: 'imap', 443: 'https',
            445: 'microsoft-ds', 993: 'imaps', 995: 'pop3s',
            1723: 'pptp', 3306: 'mysql', 3389: 'ms-wbt-server',
            5432: 'postgresql', 5900: 'vnc', 6379: 'redis',
            8080: 'http-proxy', 8443: 'https-alt', 9200: 'elasticsearch',
            27017: 'mongodb', 5000: 'docker-registry', 2375: 'docker'
        }
        return common_ports.get(port, 'unknown')
    
    def parse_ports(self, port_range):
        """Parse port range string"""
        if not port_range:
            return range(1, 1025)  # Default: common ports
        
        if '-' in port_range:
            start, end = map(int, port_range.split('-'))
            return range(start, min(end + 1, 65536))
        elif ',' in port_range:
            return [int(p) for p in port_range.split(',')]
        else:
            return [int(port_range)]
    
    def worker(self):
        """Worker thread for scanning"""
        while True:
            port = self.queue.get()
            if port is None:
                break
            
            if self.scan_type == 'syn':
                self.syn_scan(port)
            elif self.scan_type == 'udp':
                self.udp_scan(port)
            else:
                self.tcp_connect_scan(port)
            
            self.queue.task_done()
    
    def scan(self, port_range=None):
        """Main scan function"""
        print(f"\n{Fore.CYAN}📡 Target: {self.target}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔧 Scan type: {self.scan_type.upper()}")
        print(f"⚡ Threads: {self.threads}{Style.RESET_ALL}\n")
        
        ports = self.parse_ports(port_range)
        total_ports = len(ports)
        print(f"Scanning {total_ports} ports...\n")
        
        # Fill queue
        for port in ports:
            self.queue.put(port)
        
        # Start threads
        threads = []
        for _ in range(min(self.threads, total_ports)):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Wait for queue to empty
        self.queue.join()
        
        # Stop workers
        for _ in threads:
            self.queue.put(None)
        for t in threads:
            t.join()
        
        # Sort results
        self.open_ports.sort(key=lambda x: x['port'])
        
        print(f"\n{Fore.CYAN}✅ Scan completed in {time.time() - start_time:.2f} seconds")
        print(f"📊 Found {len(self.open_ports)} open ports{Style.RESET_ALL}\n")
        
        return self.open_ports
