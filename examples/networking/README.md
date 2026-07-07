# Networking Track — Web Crawling & Packet Sniffing

A side-track for a learner headed toward **web crawling** and **packet sniffing**.
It doesn't replace anything in the ten core sessions — it shows that both of those
skills are just the course fundamentals wired together, and gives you a realistic
version to grow into.

## The one rule that matters most: authorization
These are dual-use skills. Do them only where you're allowed:
- **Crawling** — obey each site's `robots.txt` and terms of service, identify your
  bot with a `User-Agent`, rate-limit yourself (one request every second or two),
  and prefer an official **API** when one exists. A crawler that ignores this is
  indistinguishable from an attack.
- **Sniffing** — capture only traffic on **your own machine or a network you're
  authorized to monitor**. Intercepting other people's traffic is illegal in many
  places. Reading a `.pcap` file you captured yourself is always fine.

Everything here is built for practice on your own sites, sandboxes
(e.g. <https://quotes.toscrape.com/>, <https://books.toscrape.com/>), and your own
captures.

## What's here
| File | Needs | What it teaches |
|---|---|---|
| `crawl_basics.py` | nothing (stdlib) | a crawler's shape on a canned website — queue + visited set + link extraction |
| `sniff_basics.py` | nothing (stdlib) | read an IPv4/TCP header out of raw **bytes** with `struct` |
| `homework/polite_crawler.py` | `requests`, `beautifulsoup4` | the real thing: live HTTP, robots.txt, rate limiting, error handling |
| `homework/packet_analyzer.py` | `scapy` | summarize real captures (or a live sniff) — top protocols, talkers, ports |

Run the two `*_basics.py` first (`python3 crawl_basics.py`) — no install, no
network. They're the simple version. Then read the `homework/` scripts: same
shape, real libraries, real caveats.

## The libraries you'll actually use
**Crawling / scraping**
- `requests` — fetch a URL over HTTP. The workhorse. (`httpx` is a modern alt.)
- `urllib.parse` — take URLs apart and rebuild them (`urljoin`, `urlparse`). stdlib.
- `urllib.robotparser` — read `robots.txt` and ask "am I allowed to fetch this?". stdlib.
- `beautifulsoup4` (`bs4`) — parse real HTML and pull out links/fields. Don't use
  regex for HTML in production.
- `time` — `sleep()` between requests. Politeness. stdlib.
- **Next step:** `scrapy` (a full crawling framework), `playwright`/`selenium`
  (for JavaScript-rendered pages).

**Sniffing / packets**
- `scapy` — capture, craft, and dissect packets; read/write `.pcap`. The Swiss army knife.
- `socket` — the low-level networking primitive under everything. stdlib.
- `struct` — unpack numbers out of raw header bytes (what `sniff_basics.py` does). stdlib.
- **Next step:** `pyshark` (Python wrapper over Wireshark's `tshark`), `dpkt`
  (fast pcap parsing), and **Wireshark** itself for eyeballing captures.

## How each session feeds these two skills
| Session | Fundamental | Crawling use | Sniffing use |
|---|---|---|---|
| 1 Types & strings | strings, f-strings | a URL is a string you build/split | format a packet summary line |
| 2 Type traps | **bytes vs str**, int/hex | decode a page's bytes to text | packets ARE bytes; ports/flags are ints in hex |
| 3 Control flow | loops, `break`/`continue` | the crawl loop; the politeness delay | the capture loop; stop after N packets |
| 4 Data structures | `set`, `deque`, `dict`, `Counter` | `visited` set + frontier queue | tally protocols/talkers with `Counter` |
| 5 Functions | functions, decorators | a `fetch()` helper; a rate-limit decorator | a `parse()` per protocol layer |
| 6 Recursion | recursion, depth limits | crawl to depth N; walk a nested sitemap/JSON | walk nested/encapsulated packet layers |
| 7 Exceptions | `try/except`, retries | timeouts, 404/500, backoff | malformed/truncated packets |
| 8 Files & libraries | `requests`, `pathlib`, `json`, APIs | **fetch pages, call JSON APIs, save results** | read/write `.pcap`, load a capture |
| 9 Regex | `re`, then `bs4` | extract links/emails/prices from text | grep fields out of log lines |
| 10 Modules & OOP | classes, generators | a `Crawler` class streaming pages lazily | a `Sniffer` class; a packet-stream generator |

Work the core sessions for the fundamentals; come back here to see them become the
two things you actually want to build.
