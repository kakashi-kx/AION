class WaybackMachine:
    """Fetch URLs from Wayback Machine with better timeout"""
    
    def __init__(self, domain):
        self.domain = domain
        self.urls = []
        
    def fetch(self):
        print_info(f"Fetching Wayback Machine URLs for {self.domain}")
        
        try:
            url = f"http://web.archive.org/cdx/search/cdx?url={self.domain}/*&output=json&fl=original&collapse=urlkey&limit=100"
            response = requests.get(url, timeout=30)  # Increased timeout
            
            if response.status_code == 200:
                data = response.json()
                
                for item in data[1:100]:  # Limit to 100 items
                    self.urls.append(item[0])
                
                print_success(f"Found {len(self.urls)} unique URLs")
                
                # Show some examples
                for url in self.urls[:5]:
                    print(f"  {G}└── {url}{RS}")
            else:
                print_warning(f"Wayback Machine returned status code: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print_warning("Wayback Machine timeout - skipping")
        except Exception as e:
            print_warning(f"Error fetching Wayback Machine data: {e}")
        
        return self.urls
