"""Utility untuk auto-detect tipe target OSINT"""
import re


def detect_target_type(target: str) -> str:
    """
    Auto-detect tipe target berdasarkan format string.
    Returns: 'email', 'domain', 'ip', 'username', 'fullname', atau 'unknown'
    """
    target = target.strip()

    # Email
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target):
        return "email"

    # IPv4
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
        parts = target.split('.')
        if all(0 <= int(p) <= 255 for p in parts):
            return "ip"

    # IPv6
    if ':' in target and re.match(r'^[0-9a-fA-F:]+$', target):
        return "ip"

    # Domain (ada titik, tidak ada spasi)
    if '.' in target and ' ' not in target and len(target.split('.')) >= 2:
        # Pastikan TLD valid
        common_tlds = ['com', 'net', 'org', 'id', 'io', 'co', 'gov', 'edu',
                       'info', 'biz', 'me', 'tv', 'ai', 'app', 'dev']
        tld = target.split('.')[-1].lower()
        if tld in common_tlds or len(tld) == 2:  # 2-char = country TLD
            return "domain"

    # Full name (mengandung spasi, kemungkinan nama orang)
    if ' ' in target and not target.startswith('http'):
        words = target.split()
        if 2 <= len(words) <= 5 and all(w.replace('.', '').isalpha() for w in words):
            return "fullname"

    # Username (satu kata, alphanumeric + beberapa karakter khusus)
    if re.match(r'^[a-zA-Z0-9._-]{3,30}$', target):
        return "username"

    return "unknown"
