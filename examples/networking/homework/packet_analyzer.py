"""packet_analyzer.py — read REAL captured packets and summarize them, with scapy.

This is the realistic homework: same idea as ../sniff_basics.py (read the fields
out of a packet), but on real captures instead of one canned byte string, and
summarized the way a network analyst actually does it — top protocols, top
talkers, top destination ports.

    pip install scapy

Two ways to run, safest first:

  1. OFFLINE from a capture file (no special rights needed) — the normal way:
         python3 packet_analyzer.py capture.pcap
     Make capture.pcap in Wireshark (File -> Save As) or `tcpdump -w capture.pcap`.

  2. LIVE from the wire (needs admin/root, and only on a network you're
     authorized to monitor — sniffing others' traffic is illegal in many places):
         sudo python3 packet_analyzer.py --live 200

The summary is pure fundamentals: a Counter per dimension (Session 4), one loop
over the packets (Session 3), a function per report (Session 5).
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter

from scapy.all import IP, TCP, UDP, rdpcap, sniff


def summarize(packets) -> dict[str, Counter]:
    """One pass over the packets, tallying each dimension into its own Counter."""
    protocols: Counter = Counter()
    talkers: Counter = Counter()       # who sends the most (by source IP)
    dst_ports: Counter = Counter()
    for pkt in packets:
        if IP in pkt:                  # scapy lets you ask "is there an IP layer?"
            talkers[pkt[IP].src] += 1
            if TCP in pkt:
                protocols["TCP"] += 1
                dst_ports[pkt[TCP].dport] += 1
            elif UDP in pkt:
                protocols["UDP"] += 1
                dst_ports[pkt[UDP].dport] += 1
            else:
                protocols[f"IP/{pkt[IP].proto}"] += 1
        else:
            protocols["non-IP"] += 1
    return {"protocols": protocols, "talkers": talkers, "dst_ports": dst_ports}


PORT_NAMES = {80: "HTTP", 443: "HTTPS", 53: "DNS", 22: "SSH", 25: "SMTP"}


def report(stats: dict[str, Counter], total: int) -> None:
    print(f"\n{total} packets captured\n")
    print("Protocols:")
    for name, n in stats["protocols"].most_common():
        print(f"  {name:<10} {n}")
    print("\nTop talkers (source IP):")
    for ip, n in stats["talkers"].most_common(5):
        print(f"  {ip:<16} {n}")
    print("\nTop destination ports:")
    for port, n in stats["dst_ports"].most_common(5):
        label = PORT_NAMES.get(port, "")
        print(f"  {port:<6} {label:<6} {n}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Summarize captured network packets.")
    ap.add_argument("pcap", nargs="?", help="a .pcap file to read (offline)")
    ap.add_argument("--live", type=int, metavar="N",
                    help="sniff N packets live instead (needs root + authorization)")
    args = ap.parse_args()

    if args.live:
        print(f"Sniffing {args.live} packets live... (Ctrl+C to stop early)")
        packets = sniff(count=args.live)     # requires admin rights
    elif args.pcap:
        packets = rdpcap(args.pcap)          # read a saved capture — no rights needed
    else:
        ap.error("give a .pcap file, or --live N")

    report(summarize(packets), len(packets))


if __name__ == "__main__":
    main()
