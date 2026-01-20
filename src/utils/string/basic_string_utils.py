import logging

logger = logging.getLogger(__name__)


class BasicStringUtils:
    """
    Author: 김대광
    """

    _is_null_or_empty = "{} is null or empty"
    _is_negative = "{} is negative"

    @staticmethod
    def is_blank(s: str) -> bool:
        """Null, 공백 체크

        Args:
            s (str): _description_

        Returns:
            _type_: _description_
        """
        return not s or not s.strip()

    @classmethod
    def default_string(cls, s: str, default_str: str) -> str:
        """Null일 경우 기본 문자열로 대체

        Args:
            s (str): _description_
            default_str (str): _description_

        Returns:
            _type_: _description_
        """
        return default_str if cls.is_blank(s) else s

    @classmethod
    def is_contains(cls, s: str, valid_chars: str) -> bool:
        """해당 문자 포함 여부 체크

        Args:
            s (str): _description_
            valid_chars (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if cls.is_blank(s):
            raise ValueError(cls._is_null_or_empty.format("s"))
        if cls.is_blank(valid_chars):
            raise ValueError(cls._is_null_or_empty.format("valid_chars"))

        return valid_chars in s

    @classmethod
    def left_pad(cls, s: str, size: int, ch: str) -> str:
        """좌측에 자리수 만큼 대체 문자 채우기

        Args:
            s (str): _description_
            size (int): _description_
            ch (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if cls.is_blank(s):
            raise ValueError(cls._is_null_or_empty.format("s"))
        if size <= 0:
            raise ValueError(cls._is_negative.format("size"))
        if not ch:
            raise ValueError(cls._is_negative.format("ch"))

        # rjust는 size가 lens(s) 보다 작거나 같으면 원래 문자열을 그대로 반환
        return s.rjust(size, ch)

    @classmethod
    def right_pad(cls, s: str, size: int, ch: str) -> str:
        """우측에 자리수 만큼 대체 문자 채우기

        Args:
            s (str): _description_
            size (int): _description_
            ch (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if cls.is_blank(s):
            raise ValueError(cls._is_null_or_empty.format("s"))
        if size <= 0:
            raise ValueError(cls._is_negative.format("size"))
        if not ch:
            raise ValueError(cls._is_negative.format("ch"))

        # ljust는 size가 lens(s) 보다 작거나 같으면 원래 문자열을 그대로 반환
        return s.ljust(size, ch)

    @classmethod
    def encode_hex(cls, s: str) -> str:
        """String To Hex

        Args:
            s (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if cls.is_blank(s):
            raise ValueError(cls._is_null_or_empty.format("s"))

        return "".join(f"{ord(c):x}" for c in s)

    @classmethod
    def decode_hex(cls, s: str) -> str:
        """Hex To String

        Args:
            s (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if cls.is_blank(s):
            raise ValueError(cls._is_null_or_empty.format("s"))

        return bytes.fromhex(s).decode("utf-8")
