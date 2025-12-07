# === scanner/dom_xss_scanner.py ===
import requests
import re

dangerous_sinks = [
    r"document\.write\s*\(", 
    r"document\.writeln\s*\(",
    r"document\.innerHTML\s*=", 
    r"innerHTML\s*=", 
    r"location\.href\s*=", 
    r"eval\s*\(",
    r"setTimeout\s*\(", 
    r"setInterval\s*\(",
    r"Function\s*\("
]

def scan(url):
    try:
        res = requests.get(url, timeout=5)
        found = []
        for sink in dangerous_sinks:
            match = re.findall(sink, res.text)
            if match:
                found.append(sink.replace(r"\s*", " ").replace(r"\\", "\\"))
        return found if found else "No dangerous sinks found"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
