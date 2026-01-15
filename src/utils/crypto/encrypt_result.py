from dataclasses import dataclass


@dataclass
class EncryptResult:
    """
    Author: 김대광
    """

    cipher_text: bytes | str
    iv: str
    tag: bytes | None = None
