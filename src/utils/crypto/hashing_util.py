import hashlib


class HashingUtil:
    """
    Author: 김대광
    """

    ORIGINAL_TEXT_IS_NULL = (
        "원본 텍스트가 비어 있거나 null입니다. 해싱을 수행할 수 없습니다."
    )

    @staticmethod
    def md5_hash(original_text: str) -> str:
        """MD5 해싱
        - SHA-1과 함께 해시 값 길이가 128비트로 낮아 권고하지 않음

        Args:
            original_text (str): _description_

        Returns:
            str: _description_
        """
        if not original_text or not original_text.strip():
            raise ValueError(HashingUtil.ORIGINAL_TEXT_IS_NULL)

        return hashlib.md5(original_text.encode()).hexdigest()

    @staticmethod
    def sha256_hash(original_text: str) -> str:
        """SHA-256 해싱
        - 해시 값 길이가 256비트로 권고

        Args:
            original_text (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not original_text or not original_text.strip():
            raise ValueError(HashingUtil.ORIGINAL_TEXT_IS_NULL)

        return hashlib.sha256(original_text.encode()).hexdigest()

    @staticmethod
    def sha512_hash(original_text: str) -> str:
        """SHA-512 해싱
        - 해시 값 길이가 512비트로 매우 권고

        Args:
            original_text (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not original_text or not original_text.strip():
            raise ValueError(HashingUtil.ORIGINAL_TEXT_IS_NULL)

        return hashlib.sha512(original_text.encode()).hexdigest()
