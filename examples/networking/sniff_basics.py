"""sniff_basics.py — read a raw packet by hand, with NO network needed.

Run me:  python3 sniff_basics.py

A "packet" is just BYTES. Sniffing is (1) capturing those bytes and (2) reading
the header fields out of them. Capturing needs admin rights and a real network
(that's homework/live_sniffer.py, using scapy). READING the bytes is pure
fundamentals, and that's what we do here on one canned IPv4 + TCP packet:
  * bytes vs str, and ints in hex          (Session 2 — the type traps)
  * slicing a bytes object                 (Session 4)
  * struct.unpack to pull out numbers      (new: the binary version of int())
"""
import struct

# One captured packet, as a hex string -> real bytes. (20-byte IPv4 header,
# then the start of a TCP header.) In a live capture these bytes come off the wire.
RAW = bytes.fromhex(
    "4500003c1c4640004006b1e6c0a80001c0a800c7"   # IPv4 header (20 bytes)
    "d431005000000000"                            # TCP: src port, dst port, ...
)


def parse_ipv4(packet: bytes) -> dict:
    """Read the fields out of an IPv4 header. Every value is an int or a str."""
    ver_ihl = packet[0]                       # one byte holds two 4-bit numbers
    version = ver_ihl >> 4                     # top 4 bits  -> 4
    header_len = (ver_ihl & 0x0F) * 4          # bottom 4 bits * 4 -> 20 bytes
    total_len = struct.unpack("!H", packet[2:4])[0]   # "!H" = big-endian uint16
    protocol = packet[9]                       # 6 = TCP, 17 = UDP, 1 = ICMP
    src = ".".join(str(b) for b in packet[12:16])     # 4 bytes -> "192.168.0.1"
    dst = ".".join(str(b) for b in packet[16:20])
    return {"version": version, "header_len": header_len, "total_len": total_len,
            "protocol": protocol, "src": src, "dst": dst}


def parse_ports(packet: bytes, ip_header_len: int) -> dict:
    """The TCP/UDP ports sit right after the IP header — two uint16s."""
    src_port, dst_port = struct.unpack("!HH", packet[ip_header_len:ip_header_len + 4])
    return {"src_port": src_port, "dst_port": dst_port}


PROTOCOLS = {1: "ICMP", 6: "TCP", 17: "UDP"}


if __name__ == "__main__":
    print("bytes vs str: RAW[0] is an int ->", RAW[0], "| hex ->", hex(RAW[0]))
    print("first 4 bytes ->", RAW[:4], "(that's a bytes object, note the b'')")

    ip = parse_ipv4(RAW)
    print("\nIPv4 header:")
    for k, v in ip.items():
        print(f"  {k:<11}: {v}")
    print(f"  protocol is {PROTOCOLS.get(ip['protocol'], '?')}")

    ports = parse_ports(RAW, ip["header_len"])
    print(f"\nTCP ports: {ports['src_port']} -> {ports['dst_port']} "
          f"(80 = HTTP, 443 = HTTPS)")
