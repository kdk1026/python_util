import base64
import gzip


class GzipCompressorUtil:
    __is_null_or_empty = "{} is null or empty"

    @classmethod
    def compress(cls, data: str) -> str:
        """문자열을 Gzip으로 압축 후 Base64 인코딩

        Args:
            data (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not data or not data.strip():
            raise ValueError(cls.__is_null_or_empty.format("data"))

        success_bytes = data.encode("utf-8")

        compressed_data = gzip.compress(success_bytes)

        return base64.b64encode(compressed_data).decode("utf-8")

    @classmethod
    def decompress(cls, compressed_data: str) -> str:
        """Base64 디코딩 후 Gzip 압축 해제

        Args:
            compressed_data (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not compressed_data or not compressed_data.strip():
            raise ValueError(cls.__is_null_or_empty.format("compressed_data"))

        decoded_bytes = base64.b64decode(compressed_data)

        decompressed_bytes = gzip.decompress(decoded_bytes)

        return decompressed_bytes.decode("utf-8")
