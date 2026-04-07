import requests
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urljoin, urlparse, urldefrag

BASE_DOMAIN = "debales.ai"
VALID_PATHS = ["blog", "product", "integration", "ai-agent"]


def clean_url(url):
    url, _ = urldefrag(url)
    return url.rstrip("/")


def extract_text(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        return text.strip() if text else ""
    except:
        return ""


def is_valid_url(url):
    parsed = urlparse(url)
    if BASE_DOMAIN not in parsed.netloc:
        return False
    if parsed.path == "":
        return True
    return any(p in parsed.path for p in VALID_PATHS)


def classify_url(url):
    url = url.lower()
    if "blog" in url:
        return "blog"
    elif "product" in url or "ai-agent" in url:
        return "product"
    elif "integration" in url:
        return "integration"
    return "general"


def get_internal_links(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        links = set()
        for a in soup.find_all("a", href=True):
            link = clean_url(urljoin(url, a["href"]))
            if is_valid_url(link):
                links.add(link)

        return list(links)
    except:
        return []


def crawl_site(start_url, max_pages=15):
    visited = set()
    to_visit = [clean_url(start_url)]
    documents = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        print(f"[SCRAPING] {url}")

        text = extract_text(url)
        if text and len(text) > 200:
            documents.append({
                "content": text,
                "metadata": {
                    "source": url,
                    "type": classify_url(url)
                }
            })

        visited.add(url)

        for link in get_internal_links(url):
            if link not in visited and link not in to_visit:
                to_visit.append(link)

    return documents