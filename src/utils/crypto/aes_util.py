import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from utils.crypto.encrypt_result import EncryptResult


class AesUtil:
    is_null = "{} is null"
    is_null_or_empty = "{} is null or empty"

    class Algorithm:
        # 과거 권장, 비권장
        AES_CBC_PKCS5PADDING = "AES/CBC/PKCS5Padding"

        # 강력 권장
        AES_GCM_NOPADDING = "AES/GCM/NoPadding"

    @staticmethod
    def generate_aes_key(key_size: int) -> bytes:
        """AES 키 생성 (16, 24, 32 바이트 가능)

        Args:
            key_size (int): _description_

        Raises:
            ValueError: _description_

        Returns:
            bytes: _description_
        """
        if key_size not in AES.key_size:
            raise ValueError("key_size must be 16, 24, or 32 byte")

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
        if not key or not key.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("key"))

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
            raise ValueError(AesUtil.is_null_or_empty.format("base64_key_string"))

        return base64.b64decode(base64_key_string)

    @staticmethod
    def encrypt(
        algorithm: str, base64_key_string: str, iv_str: str | None, plain_text: str
    ) -> EncryptResult:
        """AES 암호화

        Args:
            algorithm (str): _description_
            base64_key_string (str): _description_
            iv_str (str | None): _description_
            plain_text (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            EncryptResult: _description_
        """
        if not algorithm or not algorithm.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("algorithm"))

        if not base64_key_string or not base64_key_string.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("base64_key_string"))

        if not plain_text or not plain_text.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("plain_text"))

        key = AesUtil.convert_string_to_key(base64_key_string)

        if "CBC" in algorithm:
            if iv_str is None:
                iv = get_random_bytes(AES.block_size)
            elif isinstance(iv_str, str):
                iv = iv_str.encode("utf-8").ljust(16)[:16]

            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_data = pad(plain_text.encode("utf-8"), AES.block_size)

            cipher_text = cipher.encrypt(padded_data)
        elif "GCM" in algorithm:
            if iv_str is None:
                iv = get_random_bytes(12)
            elif isinstance(iv_str, str):
                iv = iv_str.encode("utf-8").ljust(12)[:12]

            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

            cipher_text, tag = cipher.encrypt_and_digest(plain_text.encode("utf-8"))

        generated_iv_string = base64.b64encode(iv).decode("utf-8")

        encrypt_result = EncryptResult(cipher_text, generated_iv_string, tag)
        return encrypt_result

    @staticmethod
    def decrypt(
        algorithm: str,
        base64_key_string: str,
        iv_str: str,
        is_base6_iv: bool,
        cipher_text: str,
        tag: bytes | None,
    ) -> str:
        """AES 복호화

        Args:
            algorithm (str): _description_
            base64_key_string (str): _description_
            iv_str (str): _description_
            is_base6_iv (bool): _description_
            cipher_text (str): _description_
            tag (bytes | None): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not algorithm or not algorithm.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("algorithm"))

        if not base64_key_string or not base64_key_string.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("base64_key_string"))

        if not iv_str or not iv_str.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("iv_str"))

        if not cipher_text or not cipher_text.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("cipher_text"))

        key = AesUtil.convert_string_to_key(base64_key_string)

        if "CBC" in algorithm:
            if is_base6_iv:
                iv = base64.b64decode(iv_str)
            else:
                iv = iv_str.encode("utf-8").ljust(16)[:16]

            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(cipher_text)

            try:
                return unpad(decrypted_padded, AES.block_size).decode("utf-8")
            except (ValueError, KeyError):
                return "복호화 실패: 키나 IV가 올바르지 않거나 데이터가 훼손되었습니다."

        elif "GCM" in algorithm:
            if is_base6_iv:
                iv = base64.b64decode(iv_str)
            else:
                iv = iv_str.encode("utf-8").ljust(12)[:12]

            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

            try:
                decrypted_data = cipher.decrypt_and_verify(cipher_text, tag)
                return decrypted_data.decode("utf-8")
            except ValueError:
                return "결과: 인증 실패(키가 틀리거나 데이터가 변조됨)"

    @staticmethod
    def encrypt_result_aes_gcm_java_style(
        encrypt_result: EncryptResult,
    ) -> EncryptResult:
        """AES GCM 암호화 후, 자바 스타일로 변환

        Args:
            encrypt_result (EncryptResult): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            EncryptResult: _description_
        """
        if (
            not encrypt_result.encrypted_text
            or not encrypt_result.encrypted_text.strip()
        ):
            raise ValueError(
                AesUtil.is_null_or_empty.format("encrypt_result.encrypted_text")
            )

        if not encrypt_result.iv or not encrypt_result.iv.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("encrypt_result.iv"))

        if not encrypt_result.tag:
            raise ValueError(AesUtil.is_null.format("encrypt_result.tag"))

        combined_data = encrypt_result.encrypted_text + encrypt_result.tag
        encoded_result = base64.b64encode(combined_data).decode("utf-8")

        return EncryptResult(encoded_result, encrypt_result.iv, None)

    @staticmethod
    def decrypt_aes_gcm_java_style(
        base64_key_string: str,
        iv_str: str,
        is_base6_iv: bool,
        encoded_combined: str,
    ) -> str:
        """encrypt_result_aes_gcm_java_style 결과를 복호화

        Args:
            base64_key_string (str): _description_
            iv_str (str): _description_
            is_base6_iv (bool): _description_
            encoded_combined (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not base64_key_string or not base64_key_string.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("base64_key_string"))

        if not iv_str or not iv_str.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("iv_str"))

        if not encoded_combined or not encoded_combined.strip():
            raise ValueError(AesUtil.is_null_or_empty.format("encoded_combined"))

        key = AesUtil.convert_string_to_key(base64_key_string)

        if is_base6_iv:
            iv = base64.b64decode(iv_str)
        else:
            iv = iv_str.encode("utf-8").ljust(12)[:12]

        combined_data = base64.b64decode(encoded_combined)

        tag = combined_data[-16:]
        cipher_text = combined_data[:-16]

        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

        try:
            decrypted_data = cipher.decrypt_and_verify(cipher_text, tag)
            return decrypted_data.decode("utf-8")
        except ValueError:
            return "결과: 인증 실패(키가 틀리거나 데이터가 변조됨)"
