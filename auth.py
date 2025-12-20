import hashlib

# Your secret API key
VALID_KEYS = {
    hashlib.sha256("H3ah6lcUOHj6ohwkpfMncv1vm-i1rCgMN0ZFWJrq9lQ".encode()).hexdigest()
}

def verify_key(key: str) -> bool:
    return hashlib.sha256(key.encode()).hexdigest() in VALID_KEYS
