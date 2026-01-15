import base64
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP


class RsaUtil:
    """
    Author: 김대광
    """

    _is_null = "{} is null"
    _is_null_or_empty = "{} is null or empty"

    class Convert:
        @staticmethod
        def convert_key_to_string(key_obj: RsaKey) -> str:
            """Key를 Base64 문자열로 변환

            Args:
                key_obj (bytes): _description_

            Raises:
                ValueError: _description_

            Returns:
                str: _description_
            """
            if not key_obj:
                raise ValueError(RsaUtil._is_null_or_empty.format("key"))

            # 공개키/개인키 모두 대응 (PKCS#8 권장)
            der_bytes = key_obj.export_key(format="DER", pkcs=8)

            return base64.b64encode(der_bytes).decode("utf-8")

        @staticmethod
        def convert_string_to_key(base64_key_string: str) -> bytes:
            """Base64 문자열을 Key로 변환

            Args:
                base64_key_string (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bytes: _description_
            """
            if not base64_key_string or not base64_key_string.strip():
                raise ValueError(RsaUtil._is_null_or_empty.format("base64_key_string"))

            decoded_bytes = base64.b64decode(base64_key_string)

            return RSA.import_key(decoded_bytes)

    @staticmethod
    def generate_rsa_key(key_size: int) -> RsaKey:
        """RSA 키 쌍 생성
        - keySize: 보통 2048, 3072, 4096 비트 사용 (2048비트 이상 권장)

        - private_key_obj = key
        - public_key_obj = key.publickey()

        Args:
            key_size (int): _description_

        Raises:
            ValueError: _description_

        Returns:
            bytes: _description_
        """
        if key_size not in (2048, 3072, 4096):
            raise ValueError("key_size must be 2048, 3072, or 4096 bit")

        return RSA.generate(key_size)

    @classmethod
    def encrypt(cls, public_key_obj: RsaKey, plain_text: str) -> str:
        """RSA 암호화

        Args:
            public_key_obj (RsaKey): _description_
            plain_text (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not public_key_obj:
            raise ValueError(cls._is_null_or_empty.format("public_key_obj"))

        if not plain_text or not plain_text.strip():
            raise ValueError(cls._is_null_or_empty.format("plain_text"))

        cipher = PKCS1_OAEP.new(public_key_obj, hashAlgo=SHA256)
        encrypted_bytes = cipher.encrypt(plain_text)

        return base64.b64encode(encrypted_bytes).decode("utf-8")

    @classmethod
    def decrypt(cls, private_key_obj: RsaKey, cipher_text: str) -> str:
        """RSA 복호화

        Args:
            private_key_obj (RsaKey): _description_
            cipher_text (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not private_key_obj:
            raise ValueError(cls._is_null_or_empty.format("private_key_obj"))

        if not cipher_text or not cipher_text.strip():
            raise ValueError(cls._is_null_or_empty.format("cipher_text"))

        decoded_encrypted_bytes = base64.b64decode(cipher_text)

        cipher = PKCS1_OAEP.new(private_key_obj, hashAlgo=SHA256)
        decrypted_bytes = cipher.decrypt(decoded_encrypted_bytes)

        return decrypted_bytes.decode("utf-8")
