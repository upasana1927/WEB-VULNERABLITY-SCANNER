# === scanner/header_scanner.py ===
import requests

def scan(url):
    try:
        res = requests.get(url, timeout=5)
        headers = res.headers
        required_headers = [
            'X-Frame-Options',              # Prevent clickjacking
            'Content-Security-Policy',      # Prevent XSS, injection
            'Strict-Transport-Security',    # Enforce HTTPS
            'X-Content-Type-Options',       # Prevent MIME sniffing
            'Referrer-Policy',              # Limit referrer leakage
            'Permissions-Policy',           # Restrict browser features
            'Access-Control-Allow-Origin'   # CORS setting (optional)
        ]

        missing = [h for h in required_headers if h not in headers]

        return missing if missing else "Secure"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
