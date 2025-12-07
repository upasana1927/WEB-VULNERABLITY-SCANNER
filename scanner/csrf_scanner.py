# === scanner/csrf_scanner.py ===
import requests
from bs4 import BeautifulSoup

# Common CSRF token field names
csrf_token_names = [
    "csrf", "csrf_token", "_csrf", "__csrf", "_token", "authenticity_token"
]

def scan(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        forms = soup.find_all("form")

        insecure_forms = 0

        for i, form in enumerate(forms, 1):
            method = form.get("method", "").lower()
            if method != "post":
                continue  # Only check POST forms

            inputs = form.find_all("input", {"type": "hidden"})
            token_found = False
            for inp in inputs:
                name = inp.get("name", "").lower()
                if any(token in name for token in csrf_token_names):
                    token_found = True
                    break

            if not token_found:
                print(f"[!] Form {i} may be vulnerable (no CSRF token found)")
                insecure_forms += 1

        if insecure_forms:
            return f"{insecure_forms} insecure POST form(s) detected"
        else:
            return "All POST forms contain CSRF tokens ✅"

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
