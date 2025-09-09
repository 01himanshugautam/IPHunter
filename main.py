#!/usr/bin/env python3
import subprocess
import re
import sys
import ipaddress

# Try importing dependencies, install if missing
try:
    from tabulate import tabulate
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
    from tabulate import tabulate

try:
    import psutil
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil


def get_current_subnet():
    """Detect the subnet of the active network interface."""
    addrs = psutil.net_if_addrs()
    for iface, addr_list in addrs.items():
        for addr in addr_list:
            if addr.family == 2:  # IPv4
                ip = addr.address
                netmask = addr.netmask
                if ip.startswith("127."):
                    continue
                try:
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                    return str(network)
                except Exception:
                    continue
    return None


def scan_network(subnet=None):
    try:
        if not subnet:
            subnet = get_current_subnet()
            if not subnet:
                print("❌ Could not detect current subnet.")
                return
        print(f"🔍 Scanning subnet: {subnet}\n")

        result = subprocess.run(
            ["sudo", "nmap", "-sn", subnet],
            capture_output=True, text=True, check=True
        ).stdout

        hosts = []
        current_ip, latency, mac, vendor = None, None, None, None

        for line in result.splitlines():
            if line.startswith("Nmap scan report for"):
                if current_ip:
                    hosts.append([current_ip, "Up", latency or "N/A", mac or "N/A", vendor or "N/A"])
                current_ip = line.split()[-1]
                latency, mac, vendor = None, None, None
            elif "Host is up" in line:
                latency = re.search(r"\((.*?) latency\)", line)
                latency = latency.group(1) if latency else "N/A"
            elif "MAC Address:" in line:
                parts = line.split("MAC Address:")[1].strip().split(" ", 1)
                mac = parts[0]
                vendor = parts[1].strip("()") if len(parts) > 1 else "Unknown"

        if current_ip:
            hosts.append([current_ip, "Up", latency or "N/A", mac or "N/A", vendor or "N/A"])

        headers = ["IP Address", "Status", "Latency", "MAC Address", "Vendor/Device"]
        print(tabulate(hosts, headers=headers, tablefmt="pretty"))

    except subprocess.CalledProcessError as e:
        print("Error running nmap:", e)


if __name__ == "__main__":
    scan_network()
