from datetime import datetime
import logging
import re
from urllib.parse import urlparse

from regex import F

logger = logging.getLogger(__name__)


class ValidUtil:
    """
    Author: 김대광
    """

    is_null_or_empty = "{} is null or empty"

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
    def is_length_over(cls, s: str, min: int, max: int) -> bool:
        """문자열 길이 최소/최대 길이 준수 여부

        Args:
            s (str): _description_
            min (int): _description_
            max (int): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.is_null_or_empty.format("s"))

        if min < 0 or max < 0:
            raise ValueError("min or max is less than 0.")

        str_len = len(s)
        return (str_len < min) or (str_len > max)

    @classmethod
    def is_safe_url(cls, url_str: str) -> bool:
        """URL 체크

        Args:
            url_str (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not url_str or not url_str.strip():
            raise ValueError(cls.is_null_or_empty.format("url_strs"))

        try:
            parsed = urlparse(url_str)

            if parsed.scheme:
                return parsed.scheme.lower() in ["http", "https"]

            return url_str.startswith("/")
        except Exception as e:
            logger.error(f"Unexpected error during URL check: {e}")
            return False

    class Type:
        """
        형태 체크
        """

        @staticmethod
        def is_number(s: str) -> bool:
            """숫자 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^\\d+$", s))

        @staticmethod
        def is_english(s: str) -> bool:
            """영문 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^[a-zA-Z]+$", s))

        @staticmethod
        def is_eng_blank(s: str) -> bool:
            """영문, 공백 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^[a-zA-Z\\s]+$", s))

        @staticmethod
        def is_eng_num(s: str) -> bool:
            """영문, 숫자 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^[a-zA-Z0-9]+$", s))

        @staticmethod
        def is_hangul(s: str) -> bool:
            """한글 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^[가-힣]+$", s))

        @staticmethod
        def is_han_blank(s: str) -> bool:
            """한글, 공백 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^[가-힣\\s]+$", s))

        @staticmethod
        def is_han_eng(s: str) -> bool:
            """한글, 영문 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^[가-힣a-zA-Z]+$", s))

        @staticmethod
        def is_special(s: str) -> bool:
            """문자열에 특수문자(알파벳, 숫자, 언더스코어(_), 공백을 제외한 문자)가 포함되어 있는지 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.search("[^\\w\\s]", s))

        @staticmethod
        def is_space(s: str) -> bool:
            """공백 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.search("[\\s]", s))

        @staticmethod
        def is_not_hangul(s: str) -> bool:
            """한글을 제외한 문자로만 이루어져 있는지 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("[^가-힣]+", s))

    class Format:
        """
        형식 체크
        """

        @staticmethod
        def is_email(s: str) -> bool:
            """이메일 형식 체크 (일반적인 유효성 검사)
            - 이메일 주소는 로컬 파트와 도메인 파트로 구성됩니다.
                - 로컬 파트는 영문자, 숫자, 일부 특수문자(. _ % + -)를 허용하며 점(.)으로 시작/끝나거나 연속될 수 없습니다.
                - 도메인 파트는 영문자, 숫자, 하이픈(-)을 허용하며 점(.)으로 시작/끝나거나 연속될 수 없습니다.
                - 최상위 도메인(TLD)은 최소 두 글자 이상의 영문자로 구성됩니다.

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            email_regex = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"

            return bool(re.match(email_regex, s))

        @classmethod
        def is_valid_phone_num(cls, s: str) -> bool:
            """전화번호 형식 체크
            - 휴대폰 번호
            - 일반 전화번호
            - 070 인터넷 전화(VoIP)
            - 080 수신자 부담 전화
            - 030, 050 평생번호 및 안심번호
            - 15xx, 16xx, 18xx 등 전국 대표번호

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return (
                cls.is_cell_phone_num(s)
                or cls.is_phone_num(s)
                or cls.is_internet_phone_num(s)
                or cls.is_toll_free_phone_num(s)
                or cls.is_virtual_phone_num(s)
                or cls.is_business_phone_num(s)
            )

        @staticmethod
        def is_phone_num(s: str) -> bool:
            """일반 전화번호 형식 체크
            - 02: 서울
            - 031: 경기, 032: 인천, 033: 강원
            - 041: 충남, 042: 대전, 043: 충북, 044: 세종
            - 051: 부산, 052: 울산, 053: 대구, 054: 경북, 055: 경남
            - 061: 전남, 062: 광주, 063: 전북, 064: 제주

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            cell_phone_regex = (
                "^(02|03[1-3]|04[1-4]|05[1-5]|06[1-4])-?(\\d{3,4})-?(\\d{4})$"
            )

            return bool(re.match(cell_phone_regex, s))

        @staticmethod
        def is_internet_phone_num(s: str) -> bool:
            """070 인터넷 전화(VoIP) 형식 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            cell_phone_regex = "^070-?(\\d{3,4})-?(\\d{4})$"

            return bool(re.match(cell_phone_regex, s))

        @staticmethod
        def is_toll_free_phone_num(s: str) -> bool:
            """080 수신자 부담 전화 형식 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            cell_phone_regex = "^080-?(\\d{3,4})-?(\\d{4})$"

            return bool(re.match(cell_phone_regex, s))

        @staticmethod
        def is_virtual_phone_num(s: str) -> bool:
            """030, 050 평생번호 및 안심번호 형식 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            cell_phone_regex = "^(030|050\\d)-?(\\d{3,4})-?(\\d{4})$"

            return bool(re.match(cell_phone_regex, s))

        @staticmethod
        def is_business_phone_num(s: str) -> bool:
            """15xx, 16xx, 18xx 등 전국 대표번호 형식 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            cell_phone_regex = "^^(15|16|18)\\d{2}-?\\d{4}$"

            return bool(re.match(cell_phone_regex, s))

        @staticmethod
        def is_cell_phone_num(s: str) -> bool:
            """휴대폰 번호 형식 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            cell_phone_regex = "^010-?\\d{4}-?\\d{4}$"

            return bool(re.match(cell_phone_regex, s))

        @staticmethod
        def is_company_reg_num(s: str) -> bool:
            """사업자 등록번호 형식 체크 (대한민국 3-2-5 또는 10자리 숫자 형식)
            - 하이픈(-) 유무에 관계없이 유효성을 검사합니다.
                - 예: "123-45-67890", "1234567890" 모두 유효합니다.

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            company_reg_num_regex = "^\\d{3}-?\\d{2}-?\\d{5}$"

            return bool(re.match(company_reg_num_regex, s))

        @staticmethod
        def is_ip_v4(s: str) -> bool:
            """IPv4 형식 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            # 0부터 255까지의 숫자를 나타내는 정규식 패턴
            # (?:...): 논캡처링 그룹. 성능에 약간의 이점을 줄 수 있습니다.
            IPV4_OCTET_REGEX = "(?:25[0-5]|2[0-4][\\d]|1[\\d]{2}|[1-9][\\d]|[\\d])"

            ip_v4_regex = (
                "^"
                + IPV4_OCTET_REGEX
                + "\\."
                + IPV4_OCTET_REGEX
                + "\\."
                + IPV4_OCTET_REGEX
                + "\\."
                + IPV4_OCTET_REGEX
                + "$"
            )

            return bool(re.match(ip_v4_regex, s))

        @staticmethod
        def is_yyyymmdd(s: str) -> bool:
            """YYYYMMDD 형식 체크
            - 윤년이나 월별 일수를 모두 고려하여 정확하게 날짜를 파싱하고 검증

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            if not bool(re.match("^(\\d{8}|\\d{4}-\\d{2}-\\d{2})$", s)):
                return False

            try:
                if "-" in s:
                    datetime.strptime(s, "%Y-%m-%d")
                    return True
                else:
                    datetime.strptime(s, "%Y%m%d")
                    return True
            except Exception as e:
                logger.error(e)
                return False

        @staticmethod
        def is_hh_mm(s: str) -> bool:
            """HHmm 형식 체크
            - HH:mm 형식 체크
                - re.match("^([01]\\d|2[0-3]):[0-5]\\d$", s)

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^([01]\\d|2[0-3])[0-5]\\d$", s))

        @staticmethod
        def is_hh_mm_ss(s: str) -> bool:
            """HHmmss 형식 체크
            - HH:mm:ss 형식 체크
                - re.match("^(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d$", s)

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^(?:[01]\\d|2[0-3])[0-5]\\d[0-5]\\d$", s))

        @staticmethod
        def is_yn(s: str) -> bool:
            """Y/N 형식 체크

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^[YN]$", s))

    class Account:
        """
        아이디, 비번 체크
        """

        @staticmethod
        def is_id(s: str) -> bool:
            """아이디 형식 체크
            - 첫 글자 영문
            - 7자 이상 30자 이내

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            return bool(re.match("^[a-zA-Z][a-zA-Z0-9]{6,29}$", s))

        @staticmethod
        def is_password(s: str) -> bool:
            """비밀번호 형식 체크
            - 1. 첫 글자 영문
            - 2. 첫 글자 이후 영문, 숫자, 특수문자 조합
                - 영문, 숫자, 특수문자 중 2가지 조합: 최소 10자 이상
                - 영문, 숫자, 특수문자 중 3가지 조합: 최소 8자 이상
                - 1가지 이하 조합은 유효하지 않음.

            Args:
                s (str): _description_

            Raises:
                ValueError: _description_

            Returns:
                bool: _description_
            """
            if not s or not s.strip():
                raise ValueError(ValidUtil.is_null_or_empty.format("s"))

            # 1. 첫 글자 영문 확인 및 허용 문자 검증
            if not re.match("^[a-zA-Z][a-zA-Z\\d\\W]*$", s):
                return False

            # 2. 조합 개수 확인
            has_letter = bool(re.search("[a-zA-Z]", s))  # 영문 포함 여부
            has_digit = bool(re.search("\\d", s))  # 영문 포함 여부

            # 특수문자 확인: 영문, 숫자, 언더스코어(`_`)를 제외한 문자가 있는지 확인
            has_special_char = bool(re.search("[^a-zA-Z\\d\\s]", s))

            combination_count = 0

            if has_letter:
                combination_count += 1

            if has_digit:
                combination_count += 1

            if has_special_char:
                combination_count += 1

            # 3. 길이 조건 최종 확인
            if combination_count == 2:
                return len(s) >= 10
            elif combination_count >= 3:
                return len(s) >= 8
            else:
                return False
