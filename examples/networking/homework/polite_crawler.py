"""polite_crawler.py — a small, REAL web crawler done the way it's actually done.

This is the realistic homework: same shape as ../crawl_basics.py, but it talks
to the live web and behaves. Read it, then run it on a site you're allowed to
crawl (your own, or a sandbox like https://quotes.toscrape.com/).

    pip install requests beautifulsoup4
    python3 polite_crawler.py https://quotes.toscrape.com/ --max 15

Be a good citizen — this is the difference between a crawler and a nuisance:
  * obey robots.txt (this script does, via urllib.robotparser)
  * identify yourself with a User-Agent
  * rate-limit: sleep between requests so you don't hammer the server
  * set timeouts and handle errors — the network fails constantly
  * stay on one host and cap how many pages you take
Only crawl sites you own or that permit it. When an API exists, prefer it.
"""
from __future__ import annotations

import argparse
import sys
import time
from collections import deque
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

USER_AGENT = "LearnPythonCrawler/1.0 (+educational; contact you@example.edu)"


def load_robots(root: str) -> RobotFileParser:
    """Read the site's robots.txt so we can ask it before fetching each URL."""
    rp = RobotFileParser()
    rp.set_url(urljoin(root, "/robots.txt"))
    try:
        rp.read()
    except Exception:            # no robots.txt / unreachable -> default allow
        pass
    return rp


def fetch(url: str) -> str | None:
    """Fetch one page, or return None on any network/HTTP failure (Session 7)."""
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=5)
        resp.raise_for_status()                      # turn 404/500 into an exception
        if "text/html" not in resp.headers.get("Content-Type", ""):
            return None                              # skip images, PDFs, ...
        return resp.text
    except requests.RequestException as exc:         # timeouts, DNS, 4xx/5xx, ...
        print(f"  ! {url} -> {exc}", file=sys.stderr)
        return None


def extract_links(html: str, base_url: str) -> list[str]:
    """Real HTML parsing: BeautifulSoup, not regex."""
    soup = BeautifulSoup(html, "html.parser")
    return [urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True)]


def crawl(root: str, max_pages: int, delay: float = 1.0) -> list[str]:
    host = urlparse(root).netloc
    robots = load_robots(root)
    queue: deque[str] = deque([root])
    visited: set[str] = set()
    order: list[str] = []

    while queue and len(order) < max_pages:
        url = queue.popleft()
        if url in visited or urlparse(url).netloc != host:
            continue
        visited.add(url)
        if not robots.can_fetch(USER_AGENT, url):    # respect robots.txt
            print(f"  (robots.txt disallows {url})")
            continue

        html = fetch(url)
        time.sleep(delay)                            # politeness: one request/second
        if html is None:
            continue
        order.append(url)
        print(f"  [{len(order):>3}] {url}")
        for link in extract_links(html, url):
            link, _, _ = link.partition("#")         # drop #fragments
            if link and link not in visited:
                queue.append(link)
    return order


def main() -> None:
    ap = argparse.ArgumentParser(description="A small, polite web crawler.")
    ap.add_argument("root", help="the URL to start from")
    ap.add_argument("--max", type=int, default=20, help="max pages to fetch")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    args = ap.parse_args()

    print(f"Crawling {args.root} (max {args.max} pages, {args.delay}s delay)\n")
    pages = crawl(args.root, args.max, args.delay)
    print(f"\nDone: fetched {len(pages)} pages.")


if __name__ == "__main__":
    main()
