class EncryptResult:
    def __init__(self, encrypted_text: bytes | str, iv: str, tag: bytes | None):
        self.encrypted_text = encrypted_text
        self.iv = iv
        self.tag = tag
