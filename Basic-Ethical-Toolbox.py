# // Simple Ethical Toolbox in Python made by lochlany:matrix.org

import sys
import socket

def port_scanner():
    target_ip = input("Enter IP: ")
    target_port = int(input("Enter Port: "))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    if s.connect_ex((target_ip, target_port)) == 0:
        print("Port is OPEN")
    else:
        print("Port is CLOSED")
    s.close()

def banner_grabber():
    target_ip = input("Enter IP: ")
    target_port = int(input("Enter Port: "))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((target_ip, target_port))

        s.send(b"HEAD / HTTP/1.1\r\n\r\n") 
        banner = s.recv(1024)
        print(f"Grabbed banner: {banner.decode().strip()}")
    except Exception as e:
        print(f"Could not grab banner: {e}")
    finally:
        s.close()

def subdomain_enum():
    domain = input("Enter base domain (like google.com): ")
    subdomains = ["dev", "mail", "api", "admin", "test", "blog"]
    
    print(f"Scanning {domain} for subdomains...")
    
    for sub in subdomains:
        sub_domain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(sub_domain)
            print(f"[+] Found: {sub_domain} -> {ip}")
        except:

            pass

while True:
    print("\n More tools coming soon. EXTREMELY EARLY VERSION")
    print("\n---ETHICAL TOOLBOX---")
    print("1: Port Scanner")
    print("2: Banner Grabber")
    print("3: Subdomain enum")
    print("4: Exit")
    choice = input("Select an option: ")

    if choice == "1":
        port_scanner()
    elif choice == "2":
        banner_grabber()
    elif choice == "3":
        subdomain_enum()
    elif choice == "4":
        break
    else:
        print("invalid choice")