class EncryptResult:
    def __init__(self, encrypted_text: bytes | str, iv: str, tag: bytes | None = None):
        self.cipher_text = encrypted_text
        self.iv = iv
        self.tag = tag

    def __str__(self):
        return str(self.__dict__)
