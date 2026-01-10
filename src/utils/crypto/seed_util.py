import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
from cryptography.exceptions import InvalidTag

from utils.crypto.encrypt_result import EncryptResult


class SeedUtil:
    is_null = "{} is null"
    is_null_or_empty = "{} is null or empty"

    class Algorithm:
        # 표준이며 보안성이 우수함 (권장)
        SEED_CBC_PKCS5PADDING = "SEED/CBC/PKCS7Padding"

        # 높은 보안성이 필요할 때 쓰지만 구현이 까다로움 (주의)
        SEED_GCM_NOPADDING = "SEED/GCM/NoPadding"

    @staticmethod
    def generate_seed_key() -> bytes:
        """SEED 키 생성 (16 바이트)

        Returns:
            bytes: _description_
        """
        return os.urandom(16)

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
            raise ValueError(SeedUtil.is_null_or_empty.format("key"))

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
            raise ValueError(SeedUtil.is_null_or_empty.format("base64_key_string"))

        return base64.b64decode(base64_key_string)

    @staticmethod
    def encrypt(
        algorithm: str, base64_key_string: str, plain_text: str
    ) -> EncryptResult:
        """SEED 암호화

        Args:
            algorithm (str): _description_
            base64_key_string (str): _description_
            plain_text (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            EncryptResult: _description_
        """
        if not algorithm or not algorithm.strip():
            raise ValueError(SeedUtil.is_null_or_empty.format("algorithm"))

        if not base64_key_string or not base64_key_string.strip():
            raise ValueError(SeedUtil.is_null_or_empty.format("base64_key_string"))

        if not plain_text or not plain_text.strip():
            raise ValueError(SeedUtil.is_null_or_empty.format("plain_text"))

        key = SeedUtil.convert_string_to_key(base64_key_string)

        if "CBC" in algorithm:
            iv = os.urandom(16)

            cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
            encryptor = cipher.encryptor()

            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plain_text.encode("utf-8")) + padder.finalize()

            cipher_text = encryptor.update(padded_data) + encryptor.finalize()
        elif "GCM" in algorithm:
            iv = os.urandom(12)

            cipher = Cipher(algorithms.SEED(key), modes.GCM(iv))
            encryptor = cipher.encryptor()

            cipher_text = (
                encryptor.update(plain_text.encode("utf-8")) + encryptor.finalize()
            )
            tag = encryptor.tag

        generated_iv_string = base64.b64encode(iv).decode("utf-8")

        encrypt_result = EncryptResult(cipher_text, generated_iv_string, tag)
        return encrypt_result

    @staticmethod
    def decrypt(
        algorithm: str,
        base64_key_string: str,
        base64_iv_string: str,
        cipher_text: str,
        tag: bytes | None,
    ) -> str:
        """SEED 복호화

        Args:
            algorithm (str): _description_
            base64_key_string (str): _description_
            base64_iv_string (str): _description_
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
            raise ValueError(SeedUtil.is_null_or_empty.format("algorithm"))

        if not base64_key_string or not base64_key_string.strip():
            raise ValueError(SeedUtil.is_null_or_empty.format("base64_key_string"))

        if not base64_iv_string or not base64_iv_string.strip():
            raise ValueError(SeedUtil.is_null_or_empty.format("base64_iv_string"))

        if not cipher_text or not cipher_text.strip():
            raise ValueError(SeedUtil.is_null_or_empty.format("cipher_text"))

        key = SeedUtil.convert_string_to_key(base64_key_string)
        iv = base64.b64decode(base64_iv_string)

        if "CBC" in algorithm:
            cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            decrypted_padded = decryptor.update(cipher_text) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()

            try:
                return unpadder.update(decrypted_padded) + unpadder.finalize()
            except (ValueError, KeyError):
                return "복호화 실패: 키나 IV가 올바르지 않거나 데이터가 훼손되었습니다."

        elif "GCM" in algorithm:
            cipher = Cipher(algorithms.SEED(key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()

            try:
                decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()
                return decrypted_data.decode("utf-8")
            except (InvalidTag, ValueError):
                return "결과: 인증 실패(키가 틀리거나 데이터가 변조됨)"

    @staticmethod
    def encrypt_result_seed_gcm_java_style(
        encrypt_result: EncryptResult,
    ) -> EncryptResult:
        """SEED GCM 암호화 후, 자바 스타일로 변환

        Args:
            encrypt_result (EncryptResult): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            EncryptResult: _description_
        """
        if not encrypt_result.cipher_text or not encrypt_result.cipher_text.strip():
            raise ValueError(
                SeedUtil.is_null_or_empty.format("encrypt_result.cipher_text")
            )

        if not encrypt_result.iv or not encrypt_result.iv.strip():
            raise ValueError(SeedUtil.is_null_or_empty.format("encrypt_result.iv"))

        if not encrypt_result.tag:
            raise ValueError(SeedUtil.is_null.format("encrypt_result.tag"))

        combined_data = encrypt_result.cipher_text + encrypt_result.tag
        encoded_result = base64.b64encode(combined_data).decode("utf-8")

        return EncryptResult(encoded_result, encrypt_result.iv, None)

    @staticmethod
    def decrypt_seed_gcm_java_style(
        base64_key_string: str,
        base64_iv_string: str,
        encoded_combined: str,
    ) -> str:
        """encrypt_result_aes_gcm_java_style 결과를 복호화

        Args:
            base64_key_string (str): _description_
            iv_str (str): _description_
            encoded_combined (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not base64_key_string or not base64_key_string.strip():
            raise ValueError(SeedUtil.is_null_or_empty.format("base64_key_string"))

        if not base64_iv_string or not base64_iv_string.strip():
            raise ValueError(SeedUtil.is_null_or_empty.format("base64_iv_string"))

        if not encoded_combined or not encoded_combined.strip():
            raise ValueError(SeedUtil.is_null_or_empty.format("encoded_combined"))

        key = SeedUtil.convert_string_to_key(base64_key_string)
        iv = base64.b64decode(base64_iv_string)

        combined_data = base64.b64decode(encoded_combined)

        tag = combined_data[-16:]
        cipher_text = combined_data[:-16]

        cipher = Cipher(algorithms.SEED(key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()

        try:
            decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()
            return decrypted_data.decode("utf-8")
        except (InvalidTag, ValueError):
            return "결과: 인증 실패(키가 틀리거나 데이터가 변조됨)"
