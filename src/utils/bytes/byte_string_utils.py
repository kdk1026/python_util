import logging

logger = logging.getLogger(__name__)


class ByteStringUtils:
    """
    Author: 김대광
    """

    is_null_or_empty = "{} is null or empty"
    is_negative = "{} is negative"

    @staticmethod
    def get_str_byte_length(s: str, encoding: str = "utf-8") -> int:
        """문자열의 bytes 길이 구하기

        Args:
            s (str): _description_
            encoding (str, optional): _description_. Defaults to "utf-8".

        Raises:
            ValueError: _description_

        Returns:
            int: _description_
        """
        if not s or not s.strip():
            raise ValueError(ByteStringUtils.is_null_or_empty.format("s"))

        encoding = (encoding or "utf-8").strip()

        byte_len = 0

        try:
            byte_len = len(s.encode(encoding))
        except LookupError:
            logger.error(f"지원되지 않는 인코딩입니다: {encoding}")
        except Exception as e:
            logger.error(f"알 수 없는 오류 발생: {e}", exc_info=True)

        return byte_len

    @staticmethod
    def is_byte_over(s: str, max_byte: int, encoding: str = "utf-8") -> bool:
        """문자열 바이트 최대 준수 여부

        Args:
            s (str): _description_
            max_byte (int): _description_
            encoding (str, optional): _description_. Defaults to "utf-8".

        Raises:
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not s or not s.strip():
            raise ValueError(ByteStringUtils.is_null_or_empty.format("s"))
        if max_byte < 0:
            raise ValueError(ByteStringUtils.is_negative.format("max_byte"))

        encoding = (encoding or "utf-8").strip()

        ret_flag = False

        try:
            byte_len = len(s.encode(encoding))
            ret_flag = byte_len > max_byte
        except LookupError:
            logger.error(f"지원되지 않는 인코딩입니다: {encoding}")
        except Exception as e:
            logger.error(f"알 수 없는 오류 발생: {e}", exc_info=True)

        return ret_flag

    @staticmethod
    def euc_kr_to_utf_8_string(b_org_data: bytes) -> str:
        """euc-kr 바이트 객체를 utf-8 문자열로 변환

        Args:
            b_org_data (bytes): original_text.encode('euc-kr')

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not b_org_data:
            raise ValueError(ByteStringUtils.is_null_or_empty.format("b_org_data"))

        try:
            return b_org_data.decode("euc-kr")
        except UnicodeDecodeError as e:
            print(f"Decoding error: {e}")
            return ""

    @staticmethod
    def utf_8_to_euc_kr_string(b_org_data: bytes) -> str:
        """utf-8 바이트 객체를 euc-kr 문자열로 변환

        Args:
            b_org_data (bytes): original_text.encode('utf-8')

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not b_org_data:
            raise ValueError(ByteStringUtils.is_null_or_empty.format("b_org_data"))

        try:
            return b_org_data.decode("utf-8")
        except UnicodeDecodeError as e:
            print(f"Decoding error: {e}")
            return ""

    @staticmethod
    def euc_kr_to_utf_8(b_org_data: bytes) -> bytes:
        """euc-kr 바이트 객체를 utf-8 바이트 객채로 변환

        Args:
            b_org_data (bytes): original_text.encode('euc-kr')

        Raises:
            ValueError: _description_

        Returns:
            bytes: _description_
        """
        if not b_org_data:
            raise ValueError(ByteStringUtils.is_null_or_empty.format("b_org_data"))

        try:
            return b_org_data.decode("euc-kr").encode("utf-8")
        except UnicodeDecodeError as e:
            print(f"Decoding error: {e}")
            return ""

    @staticmethod
    def utf_8_to_euc_kr(b_org_data: bytes) -> bytes:
        """utf-8 바이트 객체를 euc-kr 바이트 객체로 변환

        Args:
            b_org_data (bytes): original_text.encode('utf-8')

        Raises:
            ValueError: _description_

        Returns:
            bytes: _description_
        """
        if not b_org_data:
            raise ValueError(ByteStringUtils.is_null_or_empty.format("b_org_data"))

        try:
            return b_org_data.decode("utf-8").encode("euc-kr")
        except UnicodeDecodeError as e:
            print(f"Decoding error: {e}")
            return ""

    @staticmethod
    def substr_string(s: str, offset: int, length: int, encoding: str = "utf-8") -> str:
        """byte 단위로 문자열 자르기

        정교한 라이브러리(예: struct) 사용 권장

        Args:
            s (str): _description_
            offset (int): _description_
            length (int): _description_
            encoding (str, optional): _description_. Defaults to "utf-8".

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not s or not s.strip():
            raise ValueError(ByteStringUtils.is_null_or_empty.format("s"))
        if offset < 0:
            raise ValueError(ByteStringUtils.is_negative.format("offset"))
        if length < 0:
            raise ValueError(ByteStringUtils.is_negative.format("length"))

        encoding = (encoding or "utf-8").strip()

        try:
            full_bytes = s.encode(encoding)

            if len(full_bytes) < offset + length:
                return ""

            # 바이트 슬라이싱 [시작:끝]
            sub_bytes = full_bytes[offset : offset + length]

            return sub_bytes.decode(encoding, errors="ignore").strip()
        except LookupError:
            print(f"Unsupported encoding: {encoding}")
            return ""
