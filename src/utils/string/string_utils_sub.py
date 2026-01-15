from calendar import c
import html
import logging
import math
import uuid

logger = logging.getLogger(__name__)


class StringUtilsSub:
    """
    Author: 김대광
    """

    _is_null_or_empty = "{} is null or empty"
    _is_negative = "{} is negative"

    @staticmethod
    def get_random_string() -> str:
        """UUID 문자열에서 '-'를 제외한 32자리 문자열 반환

        Args:
            arg (_type_): _description_

        Returns:
            _type_: _description_
        """
        return uuid.uuid4().hex

    @classmethod
    def join(cls, delim: str, *args: str) -> str:
        """각 요소 사이에 지정된 구분 기호를 사용하여 문자열 배열의 모든 요소를 연결

        Args:
            delim (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not delim or not delim.strip():
            raise ValueError(cls._is_null_or_empty.format("delim"))

        return delim.join(args)

    @classmethod
    def replace_crlf_to_html_tag(cls, s: str) -> str:
        """캐리지 리턴, 라인피드 문자열을 <br/> 태그로 변환

        Args:
            s (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls._is_null_or_empty.format("s"))

        cr = "<br/>"
        return s.replace("\r\n", cr).replace("\r", cr).replace("\n", cr)

    @classmethod
    def replace_html_tag_to_crlf(cls, s: str) -> str:
        """<br/> 태그를 캐리지 리턴, 라인피드로 변환

        Args:
            s (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls._is_null_or_empty.format("s"))

        return s.replace("<br>", "\r\n").replace("<br/>", "\r\n")

    @classmethod
    def escape_xss(cls, s: str) -> str:
        """XSS 공격 대상 HTML 특수문자를 아스키 코드로 변환

        Args:
            s (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls._is_null_or_empty.format("s"))

        return html.escape(s)

    @classmethod
    def unescape_xss(cls, s: str) -> str:
        """XSS 공격 대상 아스키 코드를 HTML 특수문자로 변환

        Args:
            s (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls._is_null_or_empty.format("s"))

        return html.unescape(s)

    @classmethod
    def get_star_rating(cls, str_score: str) -> str:
        """별점 반환

        - 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0
        - 소수점 첫째자리 이하는 반올림 후 계산

        Args:
            str_score (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not str_score or not str_score.strip():
            raise ValueError(cls._is_null_or_empty.format("str_score"))

        score = round(float(str_score), 1)

        if math.isclose(score % 1, 0.5, rel_tol=1e-09, abs_tol=1e-09):
            return str(score)

        final_score = math.floor(score)
        return "0" if final_score == 0 else str(float(final_score))

    @classmethod
    def space(cls, size: int) -> str:
        """길이만큼 공백 채우기

        Args:
            size (int): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if size < 0:
            raise ValueError(cls._is_negative.format("size"))

        return " " * size
