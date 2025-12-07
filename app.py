from flask import Flask, render_template, request, send_file
from scanner import (crawler, sqli_scanner, xss_scanner, header_scanner, csrf_scanner, dom_xss_scanner)
from utils import report_generator

app = Flask(__name__)

# Common scan function
def run_scan(url_list):
    results = []
    for base_url in url_list:
        links = crawler.crawl(base_url)
        for link in links:
            results.append({
                'url': link,
                'sql_injection': sqli_scanner.scan(link),
                'xss': xss_scanner.scan(link),
                'headers': header_scanner.scan(link),
                'csrf': csrf_scanner.scan(link),
                'dom_xss': dom_xss_scanner.scan(link)
            })
    report_generator.generate_html_report(results)
    return results

# Home
@app.route("/")
def home():
    return render_template("index.html")

# Insert multiple URLs
@app.route("/insert", methods=["GET", "POST"])
def insert_page():
    results = []
    if request.method == "POST":
        url_list = request.form.getlist("urls")
        results = run_scan(url_list)
    return render_template("insert.html", results=results)

# Bulk insert URLs
@app.route("/bulk", methods=["GET", "POST"])
def bulk_page():
    results = []
    if request.method == "POST":
        urls_text = request.form.get("urls_bulk")  # must match textarea name
        url_list = [u.strip() for u in urls_text.splitlines() if u.strip()]
        results = run_scan(url_list)
    return render_template("bulk.html", results=results)

# Download report
@app.route("/download")
def download_report():
    return send_file("reports/scan_report.html", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
