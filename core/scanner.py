"""Port Scanner Module"""
class PortScanner:
    def __init__(self, target):
        self.target = target
        print(f"Scanner initialized for {target}")
    
    def scan(self, ports="1-1000"):
        print(f"Scanning {self.target} on ports {ports}")
        return {"open_ports": [80, 443, 22]}
