# 爬虫与抓包 —— 入门参考

> 写给想走向**网络爬虫**和**数据包抓取**的学习者。两者都不过是把课程里的基本功
> 拼装起来。完整可运行的示例在 `examples/networking/`。

## 首先，授权（读一遍，认真对待）
- **爬虫：** 遵守 `robots.txt` 和各网站的条款；用 `User-Agent` 表明身份；限速
  （每 1–2 秒一次请求）；有官方 **API** 就优先用 API。在自己的网站或沙盒
  （quotes.toscrape.com、books.toscrape.com）上练习。
- **抓包：** 只捕获**你自己**机器的流量，或你**获得授权**监控的网络。读自己抓的
  `.pcap` 文件永远没问题；截取他人流量在很多地方是违法的。

---

## 网络爬虫工具箱
| 库 | 作用 | 标准库？ |
|---|---|---|
| `requests` | 通过 HTTP 抓取 URL（`requests.get(url).text`） | 否（`pip install requests`） |
| `urllib.parse` | 拼接/拆解 URL —— `urljoin`、`urlparse` | 是 |
| `urllib.robotparser` | 读 `robots.txt`，用 `can_fetch()` 询问 | 是 |
| `beautifulsoup4` | 解析真实 HTML，找出链接/字段 | 否（`pip install beautifulsoup4`） |
| `time` | 请求之间 `sleep()`（礼貌） | 是 |

```python
import requests, time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

html = requests.get(url, headers={"User-Agent": "MyBot/1.0"}, timeout=5).text
soup = BeautifulSoup(html, "html.parser")
links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
time.sleep(1)                                  # 讲礼貌
```

**爬虫的骨架（第 3、4 课）：** 一个 `deque` 前沿队列 + 一个 `visited` 集合。
```python
from collections import deque
queue, visited = deque([root]), set()
while queue:
    u = queue.popleft()
    if u in visited: continue          # 集合防止无限循环
    visited.add(u)
    ... 抓取、提取链接、把同站的新链接入队 ...
```

**礼貌爬虫清单：** ☐ User-Agent  ☐ robots.txt  ☐ 超时  ☐ 请求间 sleep
☐ 只在一个站内  ☐ 限制页数  ☐ 处理 `requests.RequestException`。

**下一步：** `scrapy`（完整框架）、`playwright`/`selenium`（JS 渲染的页面）。

---

## 数据包抓取工具箱
| 库 | 作用 | 标准库？ |
|---|---|---|
| `scapy` | 捕获/构造/解析数据包，读写 `.pcap` | 否（`pip install scapy`） |
| `struct` | 从原始头部**字节**里解出数字 | 是 |
| `socket` | 底层网络原语 | 是 |

```python
from scapy.all import rdpcap, sniff, IP, TCP
packets = rdpcap("capture.pcap")               # 离线：无需特殊权限
# packets = sniff(count=100)                    # 实时：需 root + 授权
for p in packets:
    if IP in p and TCP in p:
        print(p[IP].src, "->", p[IP].dst, "port", p[TCP].dport)
```

**数据包就是字节（第 2 课——bytes 与 str 陷阱）：**
```python
import struct
raw = bytes.fromhex("4500003c...")             # 20 字节 IPv4 头部
version   = raw[0] >> 4                          # 4
hdr_len   = (raw[0] & 0x0F) * 4                  # 20 字节
total_len = struct.unpack("!H", raw[2:4])[0]     # "!H" = 大端 uint16
protocol  = raw[9]                               # 6=TCP 17=UDP 1=ICMP
src_ip    = ".".join(str(b) for b in raw[12:16]) # "192.168.0.1"
```
`b"..."`（bytes）不是 `"..."`（str）：`raw[0]` 是一个 **int**，端口和标志位都是
你常用**十六进制**读的整数。常见端口：80 HTTP · 443 HTTPS · 53 DNS · 22 SSH。

**安全抓包清单：** ☐ 只抓自己/授权网络的流量  ☐ 优先离线 `.pcap` 而非实时
☐ 实时捕获需要 admin/root  ☐ 过滤要窄（BPF：`sniff(filter="tcp port 80")`）。

**下一步：** `pyshark`（从 Python 调 Wireshark 的 tshark）、`dpkt`（快速 pcap），
以及用 **Wireshark** 本体肉眼看抓包。

---

## 每一课带你走向哪里
第 1 课 字符串 → 拼/拆 URL · **第 2 课 bytes vs str → 数据包与解码** · 第 3 课 循环 →
爬取/捕获循环 · 第 4 课 set+deque+Counter → visited 集合、前沿队列、计数 · 第 5 课
函数 → `fetch()`/`parse()` + 限速装饰器 · 第 6 课 递归 → 限深爬取、嵌套层 · 第 7 课
异常 → 超时与重试 · **第 8 课 requests/json/pathlib → 抓取、调 API、保存、读 `.pcap`** ·
第 9 课 正则→bs4 → 提取字段 · 第 10 课 类/生成器 → 惰性流式的 `Crawler`/`Sniffer`。

简单（离线）版本和真实（`requests`/`scapy`）作业都在 `examples/networking/`。
