# === scanner/crawler.py ===
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def crawl(start_url):
    visited = set()
    to_visit = [start_url]
    base_domain = urlparse(start_url).netloc

    while to_visit:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            response = requests.get(current_url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')

            for link_tag in soup.find_all('a', href=True):
                href = link_tag['href']
                full_url = urljoin(current_url, href)
                parsed_url = urlparse(full_url)

                # Only stay within the original domain
                if parsed_url.netloc == base_domain:
                    clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
                    if clean_url not in visited:
                        to_visit.append(clean_url)

        except requests.exceptions.RequestException:
            continue

    return list(visited)
