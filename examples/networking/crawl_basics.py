"""crawl_basics.py — the shape of a web crawler, with NO network needed.

Run me:  python3 crawl_basics.py

Everything here works on a canned HTML string so it runs anywhere (even in the
browser). A real crawler swaps the canned page for `requests.get(url).text` and
the regex for BeautifulSoup — see homework/polite_crawler.py for that version.

The point today: a crawler is just the course fundamentals wired together —
  * a URL is a STRING you take apart and rebuild        (Session 1)
  * a frontier QUEUE + a VISITED set                    (Sessions 3 & 4)
  * a loop that pops, fetches, finds links, enqueues    (Session 3)
"""
import re
from collections import deque
from urllib.parse import urljoin, urlparse

# A canned "website": each URL maps to its HTML. Stands in for the live web.
PAGES = {
    "https://site.test/": '<a href="/about">About</a> <a href="/team">Team</a> '
                          '<a href="https://other.test/x">external</a>',
    "https://site.test/about": '<a href="/">Home</a> <a href="/team">Team</a>',
    "https://site.test/team": '<a href="/about">About</a> <a href="mailto:x@y.z">mail</a>',
}


def fetch(url: str) -> str:
    """Return a page's HTML. The ONLY line a real crawler changes.

    Real version:  return requests.get(url, timeout=5).text
    """
    return PAGES.get(url, "")


def find_links(html: str, base_url: str) -> list[str]:
    """Pull every href out of the HTML and make it an absolute URL.

    Regex on HTML is fine for a teaching demo; a real crawler uses
    BeautifulSoup (`soup.find_all("a")`) because HTML gets messy fast.
    """
    hrefs = re.findall(r'href="([^"]+)"', html)          # Session 9
    return [urljoin(base_url, href) for href in hrefs]    # /about -> https://site.test/about


def same_site(url: str, root: str) -> bool:
    """Stay on one host — a crawler that wanders the whole web never stops."""
    return urlparse(url).netloc == urlparse(root).netloc  # Session 1: parse a URL


def crawl(root: str, max_pages: int = 10) -> list[str]:
    """Breadth-first crawl from `root`, newest fundamentals doing all the work."""
    queue = deque([root])          # the frontier: pages we still need to visit
    visited = set()                # pages we've already done — no repeats, fast lookup
    order = []
    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:         # the set is what stops infinite loops
            continue
        visited.add(url)
        order.append(url)
        for link in find_links(fetch(url), url):
            if same_site(link, root) and link not in visited:
                queue.append(link)
    return order


if __name__ == "__main__":
    print("Crawl order:")
    for i, url in enumerate(crawl("https://site.test/"), 1):
        print(f"  {i}. {url}")
    print("\nOne page's links, absolute:")
    for link in find_links(fetch("https://site.test/"), "https://site.test/"):
        keep = "keep " if same_site(link, "https://site.test/") else "skip "
        print(f"  [{keep}] {link}")
