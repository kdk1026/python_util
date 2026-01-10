import base64
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from utils.crypto.encrypt_result import EncryptResult


class TripleDesUtil:
    """
    주로 레거시 시스템과의 호환성을 위해 사용
    - NIST(미국 표준기술연구소)에서는 2023년 이후 사용을 금지하도록 권고
    """

    is_null = "{} is null"
    is_null_or_empty = "{} is null or empty"

    @staticmethod
    def generate_des_key(key_size: int) -> bytes:
        """DES 키 생성 (16, 24 바이트 가능)

        Args:
            key_size (int): _description_

        Raises:
            ValueError: _description_

        Returns:
            bytes: _description_
        """
        if key_size not in DES3.key_size:
            raise ValueError("key_size must be 16, 24 byte")
        return get_random_bytes(key_size)

    @staticmethod
    def convert_key_to_string(key: bytes) -> str:
        """키를 Base64 문자열로 변환

        Args:
            key (bytes): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not key:
            raise ValueError(TripleDesUtil.is_null_or_empty.format("key"))

        return base64.b64encode(key).decode("utf-8")

    @staticmethod
    def convert_string_to_key(base64_key_string: str) -> bytes:
        """Base64 문자열을 키로 변환

        Args:
            base64_key_string (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            bytes: _description_
        """
        if not base64_key_string or not base64_key_string.strip():
            raise ValueError(TripleDesUtil.is_null_or_empty.format("base64_key_string"))

        return base64.b64decode(base64_key_string)

    @staticmethod
    def encrypt(base64_key_string: str, iv_str: str, plain_text: str) -> EncryptResult:
        """Triple DES 암호화

        Args:
            base64_key_string (str): _description_
            iv_str (str): _description_
            plain_text (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            EncryptResult: _description_
        """
        if not base64_key_string or not base64_key_string.strip():
            raise ValueError(TripleDesUtil.is_null_or_empty.format("base64_key_string"))

        if not plain_text or not plain_text.strip():
            raise ValueError(TripleDesUtil.is_null_or_empty.format("plain_text"))

        key = TripleDesUtil.convert_string_to_key(base64_key_string)

        if iv_str is None:
            iv = get_random_bytes(DES3.block_size)
        elif isinstance(iv_str, str):
            iv = iv_str.encode("utf-8").ljust(8)[:8]

        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        padded_data = pad(plain_text.encode("utf-8"), DES3.block_size)

        cipher_text = cipher.encrypt(padded_data)

        generated_iv_string = base64.b64encode(iv).decode("utf-8")

        encrypt_result = EncryptResult(cipher_text, generated_iv_string)
        return encrypt_result

    @staticmethod
    def decrypt(
        base64_key_string: str,
        iv_str: str,
        is_base6_iv: bool,
        cipher_text: str,
    ) -> str:
        """Triple DES 복호화

        Args:
            base64_key_string (str): _description_
            iv_str (str): _description_
            is_base6_iv (bool): _description_
            cipher_text (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not base64_key_string or not base64_key_string.strip():
            raise ValueError(TripleDesUtil.is_null_or_empty.format("base64_key_string"))

        if not iv_str or not iv_str.strip():
            raise ValueError(TripleDesUtil.is_null_or_empty.format("iv_str"))

        if not cipher_text or not cipher_text.strip():
            raise ValueError(TripleDesUtil.is_null_or_empty.format("cipher_text"))

        key = TripleDesUtil.convert_string_to_key(base64_key_string)

        if is_base6_iv:
            iv = base64.b64decode(iv_str)
        else:
            iv = iv_str.encode("utf-8").ljust(16)[:16]

        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(cipher_text)

        try:
            return unpad(decrypted_padded, DES3.block_size).decode("utf-8")
        except (ValueError, KeyError):
            return "복호화 실패: 키나 IV가 올바르지 않거나 데이터가 훼손되었습니다."
