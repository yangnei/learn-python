# Crawling & Sniffing — A Starter Reference

> For the learner headed toward **web crawling** and **packet sniffing**. Both are
> just the course fundamentals wired together. Full runnable examples live in
> `examples/networking/`.

## First, authorization (read this once, mean it)
- **Crawling:** obey `robots.txt` and each site's terms; identify your bot with a
  `User-Agent`; rate-limit (1 request every 1–2s); prefer an official **API** if one
  exists. Practice on your own sites or sandboxes (quotes.toscrape.com,
  books.toscrape.com).
- **Sniffing:** capture only your **own** machine's traffic or a network you're
  **authorized** to monitor. Reading a `.pcap` you captured is always fine;
  intercepting others' traffic is illegal in many places.

---

## Web crawling toolkit
| Library | What it does | stdlib? |
|---|---|---|
| `requests` | fetch a URL over HTTP (`requests.get(url).text`) | no (`pip install requests`) |
| `urllib.parse` | build/split URLs — `urljoin`, `urlparse` | yes |
| `urllib.robotparser` | read `robots.txt`, ask `can_fetch()` | yes |
| `beautifulsoup4` | parse real HTML, find links/fields | no (`pip install beautifulsoup4`) |
| `time` | `sleep()` between requests (politeness) | yes |

```python
import requests, time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

html = requests.get(url, headers={"User-Agent": "MyBot/1.0"}, timeout=5).text
soup = BeautifulSoup(html, "html.parser")
links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
time.sleep(1)                                  # be polite
```

**The crawler shape (Sessions 3 & 4):** a `deque` frontier + a `visited` set.
```python
from collections import deque
queue, visited = deque([root]), set()
while queue:
    u = queue.popleft()
    if u in visited: continue          # the set stops infinite loops
    visited.add(u)
    ... fetch, extract links, enqueue new same-host ones ...
```

**Polite-crawl checklist:** ☐ User-Agent  ☐ robots.txt  ☐ timeout  ☐ sleep between
requests  ☐ stay on one host  ☐ cap page count  ☐ handle `requests.RequestException`.

**Next step:** `scrapy` (full framework), `playwright`/`selenium` (JS-rendered pages).

---

## Packet sniffing toolkit
| Library | What it does | stdlib? |
|---|---|---|
| `scapy` | capture / craft / dissect packets, read-write `.pcap` | no (`pip install scapy`) |
| `struct` | unpack numbers out of raw header **bytes** | yes |
| `socket` | the low-level networking primitive | yes |

```python
from scapy.all import rdpcap, sniff, IP, TCP
packets = rdpcap("capture.pcap")               # offline: no special rights
# packets = sniff(count=100)                   # live: needs root + authorization
for p in packets:
    if IP in p and TCP in p:
        print(p[IP].src, "->", p[IP].dst, "port", p[TCP].dport)
```

**A packet is just bytes (Session 2 — the bytes-vs-str trap):**
```python
import struct
raw = bytes.fromhex("4500003c...")             # 20-byte IPv4 header
version   = raw[0] >> 4                          # 4
hdr_len   = (raw[0] & 0x0F) * 4                  # 20 bytes
total_len = struct.unpack("!H", raw[2:4])[0]     # "!H" = big-endian uint16
protocol  = raw[9]                               # 6=TCP 17=UDP 1=ICMP
src_ip    = ".".join(str(b) for b in raw[12:16]) # "192.168.0.1"
```
`b"..."` (bytes) is not `"..."` (str): `raw[0]` is an **int**, ports and flags are
ints you often read in **hex**. Common ports: 80 HTTP · 443 HTTPS · 53 DNS · 22 SSH.

**Sniff-safely checklist:** ☐ your traffic / authorized network only  ☐ prefer
offline `.pcap` over live  ☐ live capture needs admin/root  ☐ filter narrowly
(BPF: `sniff(filter="tcp port 80")`).

**Next step:** `pyshark` (Wireshark's tshark from Python), `dpkt` (fast pcap), and
**Wireshark** itself to eyeball captures.

---

## Where each session takes you
S1 strings → build/split URLs · **S2 bytes vs str → packets & decoding** · S3 loops →
the crawl/capture loop · S4 set+deque+Counter → visited set, frontier, tallies · S5
functions → `fetch()`/`parse()` + a rate-limit decorator · S6 recursion → depth-limited
crawl, nested layers · S7 exceptions → timeouts & retries · **S8 requests/json/pathlib
→ fetch, call APIs, save, read `.pcap`** · S9 regex→bs4 → extract fields · S10
classes/generators → a `Crawler`/`Sniffer` streaming lazily.

See `examples/networking/` for the simple (offline) versions and the realistic
(`requests`/`scapy`) homework.
