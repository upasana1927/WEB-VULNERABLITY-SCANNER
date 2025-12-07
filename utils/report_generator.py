from jinja2 import Template
import datetime
import os

def generate_html_report(results):
    html_template = Template("""
    <html>
    <head><title>Scan Report</title></head>
    <body>
        <h2>Web Vulnerability Scan Report - {{ timestamp }}</h2>
        <table border="1">
            <tr>
                <th>URL</th>
                <th>SQLi</th>
                <th>XSS</th>
                <th>Headers</th>
            </tr>
            {% for r in results %}
            <tr>
                <td>{{ r.url }}</td>
                <td>{{ 'VULNERABLE' if r.sql_injection else 'Safe' }}</td>
                <td>{{ 'VULNERABLE' if r.xss else 'Safe' }}</td>
                <td>{{ r.headers }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """)
    os.makedirs("reports", exist_ok=True)
    output = html_template.render(results=results, timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    with open("reports/scan_report.html", "w") as f:
        f.write(output)