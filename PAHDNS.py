import sys, socket, json, urllib.request, urllib.error, ssl, hashlib, platform, base64, concurrent.futures, time, ipaddress, re, whois, dns.resolver, dns.zone, dns.query, os, subprocess
from datetime import datetime

def get_terminal_size():
    try:
        return os.get_terminal_size()
    except:
        return os.terminal_size((80, 24))

def clear_screen():
    os.system('clear')

def center_text(text, width=None):
    if width is None:
        width = get_terminal_size().columns
    return text.center(width)

def print_centered(text, color='\033[31m'):
    cols = get_terminal_size().columns
    sys.stdout.write(color + center_text(text, cols) + '\033[0m\n')

def print_centered_input(prompt):
    cols = get_terminal_size().columns
    sys.stdout.write('\033[31m' + center_text(prompt, cols) + '\033[0m')
    sys.stdout.flush()
    return input()

def flash_intro():
    clear_screen()
    sys.stdout.write('\033[?25l')
    cols, rows = get_terminal_size().columns, get_terminal_size().lines
    banner_lines = [
        "   ____    _    _   _   ____    _   _   ____  ",
        "  |  _ \\  / \\  | | | | |  _ \\  | \\ | | / ___| ",
        "  | |_) |/ _ \\ | |_| | | | | | |  \\| | \\___ \\ ",
        "  |  __// ___ \\|  _  | | |_| | | |\\  |  ___) |",
        "  |_|  /_/   \\_\\_| |_| |____/  |_| \\_| |____/ ",
        "                                               ",
        "  ETHICAL TOOLBOX  v2.0",
        "  Made by Lochlany",
        "  lochlany:matrix.org"
    ]
    centered = [center_text(line, cols) for line in banner_lines]
    vertical_padding = max(0, (rows - len(banner_lines)) // 2 - 2)
    red = '\033[31m'
    reset = '\033[0m'
    for _ in range(3):
        clear_screen()
        sys.stdout.write('\n' * vertical_padding)
        for line in centered:
            sys.stdout.write(red + line + reset + '\n')
        sys.stdout.flush()
        time.sleep(0.5)
        clear_screen()
        time.sleep(0.15)
    clear_screen()
    sys.stdout.write('\n' * vertical_padding)
    for line in centered:
        sys.stdout.write(red + line + reset + '\n')
    sys.stdout.flush()
    time.sleep(0.8)
    clear_screen()
    sys.stdout.write('\033[?25h')

def scan_single(target_ip, port, grab_banner=False):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.2)
            if s.connect_ex((target_ip, port)) == 0:
                service = socket.getservbyport(port) if port in [21,22,23,25,53,80,110,135,139,443,445,1433,3306,3389,8080,8443] else "unknown"
                banner = ""
                if grab_banner and port in [21,22,23,25,80,110,443,8080,8443]:
                    try:
                        s.send(b"HEAD / HTTP/1.0\r\n\r\n" if port in [80,443,8080,8443] else b"HELLO\r\n")
                        banner = s.recv(1024).decode(errors='ignore').strip()[:200]
                    except: pass
                return {"port": port, "service": service, "banner": banner}
    except: pass
    return None

def port_scanner():
    target = input("Target IP or hostname: ")
    try: target_ip = socket.gethostbyname(target)
    except: print("Resolve fail"); return
    print("\n1: Quick (top 20)  2: Full (1-65535)  3: Custom")
    choice = input("> ")
    if choice == "1":
        ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,3306,3389,5432,5900,8080,8443]
    elif choice == "2":
        ports = range(1,65536)
    elif choice == "3":
        try: start, end = map(int, input("Start-End (comma): ").split(',')); ports = range(start,end+1)
        except: return
    else: return
    print(f"\nScanning {target_ip} with {len(ports)} ports...")
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as ex:
        futures = {ex.submit(scan_single, target_ip, p, True): p for p in ports}
        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            if res:
                print(f"OPEN {res['port']}/{res['service']} – {res['banner'][:60]}")
                open_ports.append(res)
    print(f"\nFound {len(open_ports)} open ports.")
    if open_ports and input("Save JSON? (y/n): ").lower()=='y':
        with open(f"{target_ip}_ports.json","w") as o: json.dump(open_ports,o,indent=2)

def subdomain_enum():
    domain = input("Domain: ")
    use_file = input("Use custom wordlist file? (y/n): ").lower() == 'y'
    if use_file:
        file_path = input("Path to wordlist (one per line): ")
        try:
            with open(file_path, 'r') as f:
                wordlist = [line.strip() for line in f if line.strip()]
        except:
            print("File read fail. Using default.")
            wordlist = None
    if not use_file or not wordlist:
        wordlist = ["www","mail","api","admin","test","blog","shop","app","staging","portal","cloud","ftp","dev","secure","vpn","dashboard","status","webmail","remote","panel","server","cpanel","web","ns1","ns2","mx","smtp","pop","imap","ftp","ssh","dns","mysql","db","redis","elastic","kibana","grafana","prometheus","jenkins","git","svn","backup","cdn","media","static","img","video","download","upload","pay","shop","store","cart","help","support","docs","api2","v2","beta","dev2","stage","test2","demo","play","game","portal2","auth","login","register","signup","account","profile","user","admin2","root","sys","monitor","logs","analytics","stats","report","export","import","sync","live","stream","radio","tv","ws","socket","rpc","grpc","mqtt","kafka","zookeeper","hadoop","spark","flink","airflow","jupyter","notebook","lab","hub","wiki","confluence","jira","bitbucket","gitlab","gitea","gogs","docker","registry","kubernetes","k8s","istio","envoy","traefik","nginx","apache","tomcat","jetty","wildfly","jboss","glassfish","weblogic","websphere","oracle","mssql","postgres","mongo","couch","neo4j","influx","prom","alert","grafana2","prometheus2","thanos","loki","tempo","mimir","cortex","victoria","clickhouse","druid","pinot","kylin","doris","starrocks","presto","trino","hive","hbase","cassandra","scylla","aerospike","rethink","arangodb","orientdb","sqllite","firebird","interbase","db2","teradata","vertica","greenplum","redshift","snowflake","bigquery","databricks","cohere","openai","anthropic","huggingface","replicate","runpod","vast","lambda","coreweave","crusoe","paperspace","colab","kaggle","github","gitlab2","bitbucket2","sourceforge","codeberg","notabug","gitee","coding","aliyun","tencent","huawei","aws","azure","gcp","ibm","oraclecloud","digitalocean","linode","vultr","hetzner","ovh","scaleway","upcloud","leaseweb","hostgator","bluehost","godaddy","namecheap","cloudflare","akamai","fastly","incapsula","sucuri","stackpath","vercel","netlify","heroku","fly","render","railway","cyclic","koyeb","deno","bun","node","python","ruby","php","perl","go","rust","java","scala","clojure","elixir","erlang","haskell","lua","julia","r","matlab","octave","spss","stata","sas"]
    print(f"Brute forcing {len(wordlist)} subdomains...")
    found = []
    def check(sub):
        try:
            ip = socket.gethostbyname(f"{sub}.{domain}")
            print(f"{sub}.{domain} -> {ip}")
            return {"sub": sub, "ip": ip}
        except: return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
        for res in ex.map(check, wordlist):
            if res: found.append(res)
    print(f"Found {len(found)}.")
    if found and input("Save JSON? (y/n): ").lower()=='y':
        with open(f"{domain}_subs.json","w") as f: json.dump(found,f,indent=2)

def dns_zone_transfer():
    domain = input("Domain: ")
    try:
        ns = dns.resolver.resolve(domain, 'NS')
        for ns_rec in ns:
            ns_name = str(ns_rec.target)
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(ns_name, domain))
                if zone:
                    print(f"Zone transfer SUCCESS from {ns_name}!")
                    for name, node in zone.nodes.items():
                        print(f"  {name} -> {node.rdatasets}")
                    return
            except: pass
        print("No zone transfer possible.")
    except Exception as e: print(f"Error: {e}")

def reverse_ip_lookup():
    ip = input("IP address: ")
    try:
        import requests
        r = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=5)
        if r.text:
            domains = r.text.strip().split('\n')
            print(f"\nDomains hosted on {ip}:")
            for d in domains: print(f"  {d}")
        else: print("No domains found.")
    except: print("API failed (install requests or use curl).")

def ssl_cipher_scan():
    host = input("Hostname: ")
    port = 443
    try:
        context = ssl.create_default_context()
        context.set_ciphers('ALL:COMPLEMENTOFALL')
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ss:
                ciphers = ss.cipher()
                print(f"Cipher used: {ciphers}")
                print("Check for weak ciphers manually (e.g., RC4, NULL, EXPORT).")
    except Exception as e: print(f"Error: {e}")

def http_methods():
    url = input("URL: ")
    if not url.startswith("http"): url = "http://" + url
    methods = ['GET','HEAD','POST','PUT','DELETE','OPTIONS','TRACE','PATCH','CONNECT']
    for meth in methods:
        try:
            req = urllib.request.Request(url, method=meth)
            with urllib.request.urlopen(req, timeout=3) as resp:
                print(f"{meth} -> {resp.status}")
        except urllib.error.HTTPError as e:
            if e.code in [200,204,205,206,301,302,303,307,308]:
                print(f"{meth} -> {e.code}")
            elif e.code in [401,403,405]:
                print(f"{meth} -> {e.code} (not allowed)")
            else: print(f"{meth} -> {e.code}")
        except: pass

def whois_lookup():
    domain = input("Domain: ")
    try:
        w = whois.whois(domain)
        print(f"\n--- WHOIS ---")
        print(f"Registrar: {w.registrar}")
        print(f"Creation: {w.creation_date}")
        print(f"Expiry: {w.expiration_date}")
        print(f"Name servers: {w.name_servers}")
        if w.emails: print(f"Emails: {w.emails}")
    except: print("WHOIS failed (install python-whois)")

def email_validator():
    email = input("Email: ")
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        print("Valid format.")
        domain = email.split('@')[1]
        try:
            mx = dns.resolver.resolve(domain, 'MX')
            for r in mx: print(f"  MX: {r.exchange}")
        except: print("No MX records.")
    else: print("Invalid format.")

def crypto_tool():
    text = input("String: ").encode()
    print(f"MD5: {hashlib.md5(text).hexdigest()}")
    print(f"SHA1: {hashlib.sha1(text).hexdigest()}")
    print(f"SHA256: {hashlib.sha256(text).hexdigest()}")
    print(f"SHA512: {hashlib.sha512(text).hexdigest()}")
    print(f"Base64: {base64.b64encode(text).decode()}")
    try: print(f"Base64 decode: {base64.b64decode(text).decode(errors='ignore')}")
    except: pass

def ip_geolocation():
    target = input("IP address or domain: ")
    try:
        ip = socket.gethostbyname(target)
    except:
        print("Invalid hostname/IP")
        return
    try:
        import requests
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,mobile,proxy,hosting", timeout=5)
        data = r.json()
        if data.get('status') == 'fail':
            print(f"GeoIP API error: {data.get('message', 'unknown')}")
        else:
            print(f"\nIP: {ip}")
            print(f"Country: {data.get('country', 'N/A')}")
            print(f"Region: {data.get('regionName', 'N/A')}")
            print(f"City: {data.get('city', 'N/A')}")
            print(f"ZIP: {data.get('zip', 'N/A')}")
            print(f"Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
            print(f"ISP: {data.get('isp', 'N/A')}")
            print(f"Organization: {data.get('org', 'N/A')}")
            print(f"AS: {data.get('as', 'N/A')}")
            print(f"Mobile: {data.get('mobile', False)}")
            print(f"Proxy/VPN: {data.get('proxy', False)}")
            print(f"Hosting/DC: {data.get('hosting', False)}")
    except Exception as e:
        print(f"GeoIP failed: {e}")

def dns_record_enum():
    domain = input("Domain: ")
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'PTR', 'SRV', 'CAA']
    for rec in record_types:
        try:
            answers = dns.resolver.resolve(domain, rec)
            print(f"\n{rec} records:")
            for ans in answers:
                print(f"  {ans.to_text()}")
        except dns.resolver.NoAnswer:
            print(f"\n{rec}: No records found.")
        except dns.resolver.NXDOMAIN:
            print(f"\n{rec}: Domain does not exist.")
        except Exception as e:
            print(f"\n{rec}: Error – {e}")

def http_header_grabber():
    url = input("URL: ")
    if not url.startswith("http"): url = "http://" + url
    try:
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"\nStatus: {resp.status} {resp.reason}")
            print("Headers:")
            for k, v in resp.headers.items():
                print(f"  {k}: {v}")
    except Exception as e:
        print(f"Error: {e}")

def ssl_cert_inspector():
    host = input("Hostname: ")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ss:
                cert = ss.getpeercert()
                print(f"\n--- SSL Certificate for {host} ---")
                print(f"Subject: {dict(x[0] for x in cert.get('subject', []))}")
                print(f"Issuer: {dict(x[0] for x in cert.get('issuer', []))}")
                print(f"Not Before: {cert.get('notBefore', 'N/A')}")
                print(f"Not After: {cert.get('notAfter', 'N/A')}")
                san = cert.get('subjectAltName', [])
                if san:
                    print("Subject Alternative Names:")
                    for name in san:
                        print(f"  {name[1]}")
                print(f"Serial: {cert.get('serialNumber', 'N/A')}")
                print(f"Version: {cert.get('version', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")

def ping_sweep():
    network = input("Network CIDR (e.g., 192.168.1.0/24): ")
    try:
        net = ipaddress.ip_network(network, strict=False)
        hosts = list(net.hosts())
        print(f"Pinging {len(hosts)} hosts...")
        alive = []
        def ping(ip):
            try:
                output = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], capture_output=True, timeout=2)
                if output.returncode == 0:
                    print(f"{ip} is alive")
                    return str(ip)
            except:
                pass
            return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=150) as ex:
            results = ex.map(ping, hosts)
            for res in results:
                if res:
                    alive.append(res)
        print(f"\nFound {len(alive)} alive hosts.")
    except Exception as e:
        print(f"Error: {e}")

def cidr_converter():
    cidr = input("CIDR (e.g., 192.168.1.0/24): ")
    try:
        net = ipaddress.ip_network(cidr, strict=False)
        print(f"Network: {net.network_address}")
        print(f"Netmask: {net.netmask}")
        print(f"Broadcast: {net.broadcast_address}")
        print(f"Host range: {net.network_address + 1} - {net.broadcast_address - 1}")
        print(f"Total IPs: {net.num_addresses}")
        print(f"Usable hosts: {net.num_addresses - 2}")
    except Exception as e:
        print(f"Error: {e}")

def show_menu():
    clear_screen()
    cols, rows = get_terminal_size().columns, get_terminal_size().lines
    menu_lines = [
        "="*60,
        "ETHICAL TOOLBOX v2.0",
        "Created by lochlany:matrix.org",
        "="*60,
        " 1. Port Scanner (multi-threaded + banner)",
        " 2. Subdomain Enumerator (custom wordlist)",
        " 3. DNS Zone Transfer (AXFR) test",
        " 4. Reverse IP Lookup",
        " 5. SSL Cipher Scan",
        " 6. HTTP Method Enumerator",
        " 7. WHOIS Lookup",
        " 8. Email Validator + MX",
        " 9. Hash / Base64 Toolkit",
        "10. IP Geolocation (free API)",
        "11. DNS Record Enumerator (A, MX, NS, etc.)",
        "12. HTTP Header Grabber",
        "13. SSL Certificate Inspector",
        "14. Ping Sweep (ICMP)",
        "15. CIDR Converter",
        "16. Exit",
        "="*60,
    ]
    centered_menu = [center_text(line, cols) for line in menu_lines]
    vertical_padding = max(0, (rows - len(menu_lines)) // 2 - 1)
    sys.stdout.write('\033[31m')
    sys.stdout.write('\n' * vertical_padding)
    for line in centered_menu:
        sys.stdout.write(line + '\n')
    sys.stdout.write('\033[0m')
    sys.stdout.flush()

def main():
    flash_intro()
    while True:
        show_menu()
        choice = print_centered_input("> ")
        if choice == "1": port_scanner()
        elif choice == "2": subdomain_enum()
        elif choice == "3": dns_zone_transfer()
        elif choice == "4": reverse_ip_lookup()
        elif choice == "5": ssl_cipher_scan()
        elif choice == "6": http_methods()
        elif choice == "7": whois_lookup()
        elif choice == "8": email_validator()
        elif choice == "9": crypto_tool()
        elif choice == "10": ip_geolocation()
        elif choice == "11": dns_record_enum()
        elif choice == "12": http_header_grabber()
        elif choice == "13": ssl_cert_inspector()
        elif choice == "14": ping_sweep()
        elif choice == "15": cidr_converter()
        elif choice == "16": break
        else:
            print_centered("Invalid choice.", '\033[31m')
        print_centered("Press Enter to continue...", '\033[31m')
        input()

if __name__ == "__main__":
    main()
