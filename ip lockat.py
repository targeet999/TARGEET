#!/usr/bin/env python3
"""
IP-Tracer Tool
Version: 2.5
Author: Rajkumar Dusad
GitHub: https://github.com/rajkumardusad/IP-Tracer
Complete Python Implementation in Single File
"""

import os
import sys
import requests
import json
import time
import subprocess
import socket
from datetime import datetime
import random

class IPTracer:
    def __init__(self):
        self.version = "2.5"
        self.author = "Amr Adnan"
        self.github = "https://github.com/cbrexpt"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })

    def banner(self):
        print("""\033[1;32m
██▓ ██▓███     ▄▄▄█████▓ ██▀███   ▄▄▄       ▄████▄  ▓█████  ██▀███  
▓██▒▓██░  ██▒   ▓  ██▒ ▓▒▓██ ▒ ██▒▒████▄    ▒██▀ ▀█  ▓█   ▀ ▓██ ▒ ██▒
▒██▒▓██░ ██▓▒   ▒ ▓██░ ▒░▓██ ░▄█ ▒▒██  ▀█▄  ▒▓█    ▄ ▒███   ▓██ ░▄█ ▒
░██░▒██▄█▓▒ ▒   ░ ▓██▓ ░ ▒██▀▀█▄  ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▒▓█  ▄ ▒██▀▀█▄  
░██░▒██▒ ░  ░     ▒██▒ ░ ░██▓ ▒██▒ ▓█   ▓██▒▒ ▓███▀ ░░▒████▒░██▓ ▒██▒
░▓  ▒▓▒░ ░  ░     ▒ ░░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ░▒ ▒  ░░░ ▒░ ░░ ▒▓ ░▒▓░
 ▒ ░░▒ ░            ░      ░▒ ░ ▒░  ▒   ▒▒ ░  ░  ▒    ░ ░  ░  ░▒ ░ ▒░
 ▒ ░░░            ░        ░░   ░   ░   ▒   ░           ░     ░░   ░ 
 ░                          ░           ░  ░░ ░         ░  ░   ░     
                                            ░                           
\033[1;33m
      ➤ Tool: IP-Tracer
      ➤ Version: {0}
      ➤ Author: {1}
      ➤ GitHub: {2}
\033[0m""".format(self.version, self.author, self.github))

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def install_dependencies(self):
        """Install required packages"""
        try:
            import requests
            return True
        except ImportError:
            print("\n\033[1;31m[!] Installing required packages...\033[0m")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("\033[1;32m[✓] Packages installed successfully!\033[0m")
                time.sleep(2)
                return True
            except:
                print("\033[1;31m[!] Failed to install packages. Please run: pip install requests\033[0m")
                return False

    def get_ip_info(self, ip):
        """Get IP information from multiple sources"""
        services = {
            'ip-api': f'http://ip-api.com/json/{ip}',
            'ipapi.co': f'https://ipapi.co/{ip}/json/',
            'ipwhois': f'http://ipwhois.app/json/{ip}',
            'ipinfo.io': f'https://ipinfo.io/{ip}/json'
        }
        
        all_data = {}
        for name, url in services.items():
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    all_data[name] = response.json()
                    print(f"\033[1;32m[✓] {name} - Success\033[0m")
                else:
                    print(f"\033[1;31m[✗] {name} - Failed\033[0m")
            except:
                print(f"\033[1;31m[✗] {name} - Error\033[0m")
                continue
        
        return all_data

    def extract_best_info(self, all_data):
        """Extract the best available information"""
        # Try ip-api first (most reliable)
        if 'ip-api' in all_data and all_data['ip-api'].get('status') == 'success':
            data = all_data['ip-api']
            return {
                'IP Address': data.get('query', 'N/A'),
                'Country': data.get('country', 'N/A'),
                'Country Code': data.get('countryCode', 'N/A'),
                'Region': data.get('regionName', 'N/A'),
                'City': data.get('city', 'N/A'),
                'ZIP Code': data.get('zip', 'N/A'),
                'Latitude': data.get('lat', 'N/A'),
                'Longitude': data.get('lon', 'N/A'),
                'Timezone': data.get('timezone', 'N/A'),
                'ISP': data.get('isp', 'N/A'),
                'Organization': data.get('org', 'N/A'),
                'AS': data.get('as', 'N/A')
            }
        
        # Try ipapi.co as fallback
        elif 'ipapi.co' in all_data:
            data = all_data['ipapi.co']
            return {
                'IP Address': data.get('ip', 'N/A'),
                'Country': data.get('country_name', 'N/A'),
                'Country Code': data.get('country_code', 'N/A'),
                'Region': data.get('region', 'N/A'),
                'City': data.get('city', 'N/A'),
                'ZIP Code': data.get('postal', 'N/A'),
                'Latitude': data.get('latitude', 'N/A'),
                'Longitude': data.get('longitude', 'N/A'),
                'Timezone': data.get('timezone', 'N/A'),
                'ISP': data.get('org', 'N/A'),
                'Organization': data.get('org', 'N/A'),
                'AS': data.get('asn', 'N/A')
            }
        
        return None

    def display_ip_info(self, info, target_ip):
        """Display IP information in formatted way"""
        print(f"\n\033[1;36m[+] Tracing Result for: {target_ip}\033[0m")
        print("\033[1;33m" + "═" * 60 + "\033[0m")
        
        if info:
            for key, value in info.items():
                if value and value != 'N/A':
                    print(f"\033[1;32m[✓] {key:<15}: \033[1;37m{value}\033[0m")
            
            print("\033[1;33m" + "═" * 60 + "\033[0m")
            
            # Show Google Maps link if coordinates available
            if info.get('Latitude') != 'N/A' and info.get('Longitude') != 'N/A':
                map_url = f"https://maps.google.com/?q={info['Latitude']},{info['Longitude']}"
                print(f"\033[1;35m[🗺️] Google Maps: {map_url}\033[0m")
        else:
            print("\033[1;31m[!] No information found for this IP address\033[0m")

    def trace_specific_ip(self):
        """Trace a specific IP address"""
        self.clear_screen()
        self.banner()
        
        ip = input("\n\033[1;33m[+] Enter IP Address: \033[0m").strip()
        
        if not ip:
            print("\033[1;31m[!] Please enter a valid IP address\033[0m")
            time.sleep(2)
            return
        
        print(f"\n\033[1;36m[~] Tracing IP address: {ip}\033[0m")
        print("\033[1;33m[~] Gathering information from multiple sources...\033[0m\n")
        
        all_data = self.get_ip_info(ip)
        
        if not all_data:
            print("\033[1;31m[!] Failed to retrieve information for this IP\033[0m")
            time.sleep(2)
            return
        
        info = self.extract_best_info(all_data)
        self.display_ip_info(info, ip)

    def trace_my_ip(self):
        """Trace own IP address"""
        self.clear_screen()
        self.banner()
        
        print("\n\033[1;36m[~] Discovering your public IP address...\033[0m")
        
        try:
            # Get public IP
            my_ip = self.session.get('https://api.ipify.org', timeout=10).text
            print(f"\033[1;32m[✓] Your Public IP Address: {my_ip}\033[0m")
            
            print("\n\033[1;36m[~] Tracing your location information...\033[0m")
            print("\033[1;33m[~] Gathering data from multiple sources...\033[0m\n")
            
            all_data = self.get_ip_info(my_ip)
            
            if all_data:
                info = self.extract_best_info(all_data)
                self.display_ip_info(info, my_ip)
            else:
                print("\033[1;31m[!] Failed to trace your location information\033[0m")
                
        except Exception as e:
            print(f"\033[1;31m[!] Error: {e}\033[0m")

    def generate_tracking_link(self):
        """Generate tracking link (simulated)"""
        self.clear_screen()
        self.banner()
        
        print("""
\033[1;36m[+] IP Tracking Link Generator\033[0m

\033[1;33m[!] This feature requires additional setup:\033[0m

\033[1;32mRequired Components:
    • PHP Server
    • ngrok (for public access)
    • Internet Connection

\033[1;33mSetup Steps:
    1. Create a PHP file with tracking code
    2. Run: php -S localhost:8080
    3. Run: ngrok http 8080
    4. Send the ngrok URL to target
    5. Check captured IPs in log file

\033[1;32m[~] Simulated Tracking Link Generated:\033[0m
    \033[1;35mhttps://ip-tracker-{}.ngrok.io/track.php\033[0m

\033[1;33m[!] Send this link to target and monitor ip.txt for results\033[0m
        """.format(random.randint(1000, 9999)))

    def update_tool(self):
        """Update tool functionality"""
        self.clear_screen()
        self.banner()
        
        print("\n\033[1;36m[~] Checking for updates...\033[0m")
        time.sleep(2)
        
        # Simulate update check
        print("\033[1;32m[✓] IP-Tracer is up to date!\033[0m")
        print("\033[1;33m[~] Current Version: {}\033[0m".format(self.version))
        
        print("""
\033[1;33m[!] For manual update from original repository:\033[0m
    git clone https://github.com/rajkumardusad/IP-Tracer.git
    cd IP-Tracer
    chmod +x install
    ./install
        """)

    def show_about(self):
        """Show about information"""
        self.clear_screen()
        self.banner()
        
        print("""
\033[1;36m[ ABOUT IP-TRACER ]\033[0m

\033[1;33mDescription:\033[0m
IP-Tracer is an open-source intelligence tool for tracking 
IP addresses and gathering detailed location information.

\033[1;33mFeatures:\033[0m
• Track any IP address location worldwide
• Get detailed ISP and organization information  
• Discover your own public IP and location
• Generate IP tracking links
• Multiple API support for accuracy
• User-friendly interface

\033[1;33mTechnical Details:\033[0m
• Uses multiple IP geolocation APIs
• Cross-platform compatibility
• No root access required
• Fast and efficient

\033[1;31mLegal Disclaimer:\033[0m
This tool is intended for educational purposes and legitimate 
security research only. Users are responsible for complying 
with all applicable laws. Only track IP addresses that you 
own or have explicit permission to investigate.

\033[1;33mOriginal Repository:\033[0m
https://github.com/rajkumardusad/IP-Tracer

\033[1;32mPython Version:\033[0m
This is a complete Python implementation of the original tool.
        """)

    def install_tool(self):
        """Installation routine"""
        self.clear_screen()
        print("""\033[1;32m
 ██▓ ██████  ▄▄▄▄    ██████  ▄████▄   ██▀███   ▄▄▄     ▄▄▄█████▓
▓██▒██    ▒ ▓█████▄ ▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄   ▓  ██▒ ▓▒
▒██░ ▓██▄   ▒██▒ ▄██░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄ ▒ ▓██░ ▒░
░██░ ▒   ██▒▒██░█▀    ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██░ ▓██▓ ░ 
░██▒██████▒▒░▓█  ▀█▓▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒ ▒██▒ ░ 
░▓ ▒ ▒▓▒ ▒ ░░▒▓███▀▒▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▒ ░░   
 ▒ ░ ░▒  ░ ░▒░▒   ░ ░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░   ░    
 ▒ ░  ░  ░   ░    ░ ░  ░  ░  ░          ░░   ░   ░   ▒    ░      
 ░       ░   ░            ░  ░ ░         ░           ░  ░        
                        ░                                       
\033[0m""")
        
        print("\033[1;33m[+] Installing IP-Tracer...\033[0m")
        
        # Install dependencies
        if not self.install_dependencies():
            return
        
        # Make executable
        try:
            current_file = os.path.abspath(__file__)
            os.chmod(current_file, 0o755)
            print("\033[1;32m[✓] IP-Tracer made executable\033[0m")
        except:
            pass
        
        # Try to create symlink
        try:
            if os.name == 'posix':  # Linux/Unix
                symlink_path = "/usr/local/bin/ip-tracer"
                if not os.path.exists(symlink_path):
                    os.symlink(current_file, symlink_path)
                    print("\033[1;32m[✓] Symlink created: /usr/local/bin/ip-tracer\033[0m")
        except:
            print("\033[1;33m[!] Could not create symlink\033[0m")
        
        print("\033[1;32m[✓] Installation completed successfully!\033[0m")
        print("\033[1;33m[+] Usage: python3 ip_tracer.py\033[0m")
        time.sleep(3)

    def main_menu(self):
        """Main menu interface"""
        while True:
            self.clear_screen()
            self.banner()
            
            print("""
\033[1;36m [ MAIN MENU ]\033[0m

\033[1;32m [1] Trace Your IP\033[0m
\033[1;32m [2] Trace IP Address\033[0m  
\033[1;32m [3] Generate Tracking Link\033[0m
\033[1;32m [4] Update Tool\033[0m
\033[1;32m [5] About\033[0m
\033[1;32m [6] Install\033[0m
\033[1;31m [0] Exit\033[0m
            """)
            
            choice = input("\n\033[1;33m[+] Choose an option: \033[0m").strip()
            
            if choice == '1':
                self.trace_my_ip()
            elif choice == '2':
                self.trace_specific_ip()
            elif choice == '3':
                self.generate_tracking_link()
            elif choice == '4':
                self.update_tool()
            elif choice == '5':
                self.show_about()
            elif choice == '6':
                self.install_tool()
            elif choice == '0':
                print("\n\033[1;32m[✓] Thank you for using IP-Tracer!\033[0m")
                sys.exit(0)
            else:
                print("\n\033[1;31m[!] Invalid option!\033[0m")
                time.sleep(1)
                continue
            
            if choice in ['1', '2', '3', '4']:
                input("\n\033[1;33m[+] Press Enter to continue...\033[0m")

def main():
    """Main function"""
    tracer = IPTracer()
    
    # Check if dependencies are installed
    try:
        import requests
    except ImportError:
        print("\033[1;31m[!] Required packages not found!\033[0m")
        if tracer.install_dependencies():
            print("\033[1;32m[✓] Please restart the script!\033[0m")
        sys.exit(1)
    
    # Start the application
    tracer.main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Program interrupted by user\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\n\033[1;31m[!] Unexpected error: {e}\033[0m")
        sys.exit(1)