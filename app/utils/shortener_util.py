import hashlib


def generate_short_url(original_url: str, length: int = 10) -> str:
    hash = hashlib.sha256(original_url.encode())
    return hash.hexdigest()[:length]
