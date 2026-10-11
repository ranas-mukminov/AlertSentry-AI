"""Validate alert entities before sending them to third-party threat intel.

Alert fields come from SIEMs and webhooks and are not trusted. Only globally
routable IPs and well-formed hashes are worth looking up: private/internal
addresses would be leaked to VirusTotal/AbuseIPDB (and burn API quota), and an
unvalidated string is interpolated into the VirusTotal URL path and cache key.
"""

from __future__ import annotations

import ipaddress
import re
from typing import Optional

# MD5, SHA-1, SHA-256
_HASH_RE = re.compile(r"^(?:[0-9a-f]{32}|[0-9a-f]{40}|[0-9a-f]{64})$")


def public_ip(value: Optional[str]) -> Optional[str]:
    """Return the canonical form of a globally routable IP, else None."""
    if not value:
        return None
    try:
        ip = ipaddress.ip_address(value.strip())
    except ValueError:
        return None
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        ip = ip.ipv4_mapped
    return str(ip) if ip.is_global else None


def file_hash(value: Optional[str]) -> Optional[str]:
    """Return a lowercase MD5/SHA-1/SHA-256 hex digest, else None."""
    if not value:
        return None
    digest = value.strip().lower()
    return digest if _HASH_RE.fullmatch(digest) else None
