from dataclasses import dataclass


@dataclass
class EncryptResult:
    cipher_text: bytes | str
    iv: str
    tag: bytes | None = None
