# IPHunter 🎯  
_Automatic Subnet Detection & Network Scanner (Python + Nmap)_

## 📖 Overview
**IPHunter** is a Python tool that:
- Automatically detects your **current WiFi/LAN subnet**  
- Runs a **ping sweep** using `nmap`  
- Collects **IP, MAC, latency, and vendor details**  
- Displays results in a clean, readable **table format**

Useful for:
- Finding devices connected to your WiFi  
- Identifying unknown devices on your network  
- Quick local network inventory  

---

## ⚡ Features
- ✅ Auto-detects active subnet (no need to hardcode)  
- ✅ Clean tabular output using `tabulate`  
- ✅ Shows MAC address & vendor if available  
- ✅ Works on Linux, macOS, and Windows (with Nmap installed)  
- 🚀 Optional: Save results to CSV/JSON (coming soon)  

---

## 🛠 Installation

### 1. Clone this repo
```bash
git clone https://github.com/01himanshugautam/IPHunter
cd IPHunter
