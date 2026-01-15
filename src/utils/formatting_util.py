import re


class FormattingUtil:
    """
    Author: 김대광
    """

    __is_null_or_empty = "{} is null or empty"

    __FORMAT_HYPHEN = r"\1-\2-\3"
    __FORMAT_NOT_HYPHEN = r"\1\2\3"

    __FORMAT_BIZ_HYPHEN = r"\1\2-\3"
    __FORMAT_BIZ_NOT_HYPHEN = r"\12\3"

    @classmethod
    def make_basic_phone_num(cls, s: str, is_hyphen: bool) -> str | None:
        """일반 전환번호 포맷
        - 0x(x)-xxx(x)-xxxx

        Args:
            s (str): _description_
            is_hyphen (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            str | None: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.__is_null_or_empty.format("s"))

        pattern = "^(02|03[1-3]|04[1-4]|05[1-5]|06[1-4])-?(\\d{3,4})-?(\\d{4})$"
        if not re.match(pattern, s):
            return None

        replacement = cls.__FORMAT_HYPHEN if is_hyphen else cls.__FORMAT_NOT_HYPHEN
        return re.sub(pattern, replacement, s)

    @classmethod
    def make_internet_phone_num(cls, s: str, is_hyphen: bool) -> str | None:
        """070 인터넷 전화(VoIP) 포맷
        - 070-xxx(x)-xxxx

        Args:
            s (str): _description_
            is_hyphen (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            str | None: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.__is_null_or_empty.format("s"))

        pattern = "^(070)-?(\\d{3,4})-?(\\d{4})$"
        if not re.match(pattern, s):
            return None

        replacement = cls.__FORMAT_HYPHEN if is_hyphen else cls.__FORMAT_NOT_HYPHEN
        return re.sub(pattern, replacement, s)

    @classmethod
    def make_toll_free_phone_num(cls, s: str, is_hyphen: bool) -> str | None:
        """080 수신자 부담 전화 포맷
        - 080-xxx(x)-xxxx

        Args:
            s (str): _description_
            is_hyphen (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            str | None: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.__is_null_or_empty.format("s"))

        pattern = "^(080)-?(\\d{3,4})-?(\\d{4})$"
        if not re.match(pattern, s):
            return None

        replacement = cls.__FORMAT_HYPHEN if is_hyphen else cls.__FORMAT_NOT_HYPHEN
        return re.sub(pattern, replacement, s)

    @classmethod
    def make_virtual_phone_num(cls, s: str, is_hyphen: bool) -> str | None:
        """030, 050 평생번호 및 안심번호 포맷
        - 030|050-xxx(x)-xxxx

        Args:
            s (str): _description_
            is_hyphen (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            str | None: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.__is_null_or_empty.format("s"))

        pattern = "^(030|050\\d)-?(\\d{3,4})-?(\\d{4})$"
        if not re.match(pattern, s):
            return None

        replacement = cls.__FORMAT_HYPHEN if is_hyphen else cls.__FORMAT_NOT_HYPHEN
        return re.sub(pattern, replacement, s)

    @classmethod
    def make_business_phone_num(cls, s: str, is_hyphen: bool) -> str | None:
        """15xx, 16xx, 18xx 등 전국 대표번호 포맷
        - 15|16|18xx-xxxx

        Args:
            s (str): _description_
            is_hyphen (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            str | None: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.__is_null_or_empty.format("s"))

        pattern = "^(15|16|18)(\\d{2})-?(\\d{4})$"
        if not re.match(pattern, s):
            return None

        replacement = (
            cls.__FORMAT_BIZ_HYPHEN if is_hyphen else cls.__FORMAT_BIZ_NOT_HYPHEN
        )
        return re.sub(pattern, replacement, s)

    @classmethod
    def make_cell_phone_num(cls, s: str, is_hyphen: bool) -> str | None:
        """휴대폰 번호 포맷
        - 01x-xxx(x)-xxxx

        Args:
            s (str): _description_
            is_hyphen (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            str | None: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.__is_null_or_empty.format("s"))

        pattern = "^(01[016789])-?(\\d{3,4})-?(\\d{4})$"
        if not re.match(pattern, s):
            return None

        replacement = cls.__FORMAT_HYPHEN if is_hyphen else cls.__FORMAT_NOT_HYPHEN
        return re.sub(pattern, replacement, s)

    @classmethod
    def make_business_reg_num(cls, s: str, is_hyphen: bool) -> str | None:
        """사업자 등록번호 포맷
        - xxx-xx-xxxxx

        Args:
            s (str): _description_
            is_hyphen (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            str | None: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.__is_null_or_empty.format("s"))

        pattern = "^(\\d{3})-?(\\d{2})-?(\\d{5})$"
        if not re.match(pattern, s):
            return None

        replacement = cls.__FORMAT_HYPHEN if is_hyphen else cls.__FORMAT_NOT_HYPHEN
        return re.sub(pattern, replacement, s)

    @classmethod
    def make_yyyy_mm_dd(cls, s: str, is_hyphen: bool) -> str | None:
        """날짜 포맷
        - YYYY-MM-DD

        Args:
            s (str): _description_
            is_hyphen (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            str | None: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.__is_null_or_empty.format("s"))

        date_pattern = "^(\\d{4})[\\-/. ]?(\\d{2})[\\-/. ]?(\\d{2})$"

        match = re.match(date_pattern, s)

        if not match:
            return None

        year, month, day = match.groups()

        if is_hyphen:
            return f"{year}-{month}-{day}"
        else:
            return f"{year}{month}{day}"

    @classmethod
    def make_card_no(cls, s: str, is_hyphen: bool) -> str | None:
        """카드번호 포맷
        - (16자리) ####-####-####-####
        - (15자리) ####-######-#####

        Args:
            s (str): _description_
            is_hyphen (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            str | None: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.__is_null_or_empty.format("s"))

        length = len(s)
        if length == 16:
            pattern = "^(\\d{4})-?(\\d{4})-?(\\d{4})-?(\\d{4})$"
            replacement = r"\1-\2-\3-\4" if is_hyphen else "\1\2\3\4"
        elif length == 15:
            pattern = "^(\\d{4})-?(\\d{6})-?(\\d{5})$"
            replacement = cls.__FORMAT_HYPHEN if is_hyphen else cls.__FORMAT_NOT_HYPHEN

        if not re.match(pattern, s):
            return None

        return re.sub(pattern, replacement, s)

    @staticmethod
    def convert_money_format(num: int) -> str:
        """수치를 금액 표현으로 변환
        - #,###

        Args:
            num (int): _description_

        Returns:
            str: _description_
        """
        return f"{num:,}"

    @classmethod
    def convert_money_hangul(cls, s: str) -> str:
        """숫자금액 문자열을 한글 금액 표현으로 변환

        Args:
            s (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not s or not s.strip():
            raise ValueError(cls.__is_null_or_empty.format("s"))

        money_str = s.replace(",", "")
        if not money_str.isdigit():
            return ""

        units = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
        small_units = ["", "십", "백", "천"]
        large_units = ["", "만", "억", "조", "경"]

        result = []
        length = len(money_str)

        for i, char in enumerate(money_str):
            digit = int(char)
            rev_idx = length - 1 - i
            q, r = divmod(rev_idx, 4)

            if digit > 0:
                if not (digit == 1 and r != 0):
                    result.append(units[digit])
                result.append(small_units[r])

            start_idx = max(0, i - 3)
            section = s[start_idx : i + 1]

            if r == 0 and int(section) > 0:
                result.append(large_units[q])

        return "".join(result) + "원" if result else ""
