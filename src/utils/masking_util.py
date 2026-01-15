import ipaddress
import re
from turtle import st


class MaskingUtil:
    """
    Author: 김대광
    """

    @classmethod
    def mask_name(cls, name: str) -> str:
        """이름 마스킹
        - 한글
            - 2글자 첫자리 제외한 마스킹
            - 첫자리, 마지막자리 제외한 마스킹
        - 영문
            - 4자리 이하 : 앞 2자리 제외하고 마스킹
            - 4자리 이상 : 앞 4자리 제외하고 마스킹

        Args:
            name (str): _description_

        Returns:
            str: _description_
        """
        if not name or not name.strip():
            return ""

        if len(name) > 50:
            return name

        regex = "[ㄱ-ㅎㅏ-ㅣ가-힣]+"

        if re.match(regex, name):
            return cls.__mask_korean_name(name)
        else:
            return cls.__mask_english_name(name)

    @classmethod
    def __mask_korean_name(cls, name: str) -> str:
        length = len(name)
        first_char = name[0]

        if length == 2:
            return first_char + "*"

        last_char = name[-1]

        masked_middle = "*" * (length - 2) if length > 2 else ""

        return first_char + masked_middle + last_char

    @classmethod
    def __mask_english_name(cls, name: str) -> str:
        length = len(name)

        if length <= 4:
            return name[: length - 2] + "**"
        else:
            return name[:4] + "*" * (length - 4)

    @staticmethod
    def mask_rrn(rrn: str, is_show_gender: bool) -> str:
        """주민등록번호 마스킹 (하이픈 포함)
        - 뒷자리 마스킹

        Args:
            rrn (str): _description_
            is_show_gender (bool): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not rrn or len(rrn) != 14 or rrn[6] != "-":
            raise ValueError("Invalid Resident Registration Number")

        if is_show_gender:
            # 성별 숫자까지 표시
            return rrn[:8] + "******"
        else:
            # 뒷자리 전체 마스킹
            return rrn[:7] + "*******"

    @staticmethod
    def mask_passport_number(passport_number: str) -> str:
        """여권번호 마스킹
        - 뒤 4자리 마스킹

        Args:
            passport_number (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not passport_number or len(passport_number) < 5:
            raise ValueError("Invalid Passport Number")

        length = len(passport_number)
        masked_middle = "*" * (length - 4) if length > 4 else ""

        return passport_number[:4] + masked_middle

    @staticmethod
    def mask_phone_num(phone_number: str) -> str:
        """전화번호 마스킹
        - 가운데 부분 마스킹

        - 일반 전화번호
        - 070 인터넷 전화(VoIP)
        - 080 수신자 부담 전화
        - 030, 050 평생번호 및 안심번호
        - 휴대폰 번호

        Args:
            phone_number (str): _description_

        Returns:
            str: _description_
        """
        if not phone_number or not phone_number.strip():
            return ""

        clean_num = phone_number.replace("-", "")
        length = len(clean_num)

        if length >= 9:
            last = clean_num[: length - 4]

            first_part_end_idx = 2 if clean_num.startswith("02") else 3
            first = clean_num[:first_part_end_idx]

            middle_part = clean_num[first_part_end_idx : length - 4]

            masked_middle = "*" * len(middle_part)

            return f"{first}-{masked_middle}-{last}"

        return phone_number

    @staticmethod
    def mask_id(id: str) -> str:
        """아이디 마스킹
        - 4번째 자리부터 마스킹

        Args:
            id (str): _description_

        Returns:
            str: _description_
        """
        if not id or not id.strip():
            return ""

        length = len(id)

        if length <= 3:
            return id
        else:
            repeat_count = length - 3
            masked_stars = "*" * repeat_count

        return id[:3] + masked_stars

    @classmethod
    def mask_email(cls, email: str) -> str:
        """이메일 마스킹
        - ID 4번재 자리부터 마스킹

        Args:
            email (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not email or not email.strip():
            return ""

        at_index = email.find("@")

        if at_index < 1:
            raise ValueError("Invalid email address")

        id_part = email[:at_index]
        domain_part = email[at_index:]

        masked_id_part = cls.mask_id(id_part)

        return masked_id_part + domain_part

    @staticmethod
    def mask_road_address(address: str) -> str:
        """주소 마스킹
        - 도로명 이하의 건물번호 및 상세주소의 숫자

        Args:
            address (str): _description_

        Returns:
            str: _description_
        """
        if not address or not address.strip():
            return ""

        return re.sub("\\d", "*", address)

    @classmethod
    def mask_card_number(cls, card_number: str, start_index: int) -> str:
        """카드번호 마스킹
        - start_index (7 or 9)
        - 일반적으로 15/16자리 중 7번째부터 12번째 숫자 (혹은 9번째부터 12번째 숫자)를 마스킹

        Args:
            card_number (str): _description_
            start_index (int): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not card_number or not card_number.strip():
            return ""

        if start_index not in [7, 9]:
            raise ValueError("Invalid start index. It should be either 7 or 9.")

        digits_only = re.sub("[^\\d]", "", card_number)
        length = len(digits_only)

        chars = list(digits_only)

        # 마스킹 제한 설정 (7일 때 6개, 9일 때 4개)
        mask_limit = 6 if start_index == 7 else 4
        masked_so_far = 0

        for i in range(len(chars)):
            if (i + 1) >= start_index and masked_so_far < mask_limit:
                chars[i] = "*"
                masked_so_far += 1

        masked_str = "".join(chars)

        return cls.__format_by_length(masked_str, length)

    @staticmethod
    def __format_by_length(masked_str, length):
        if length == 16:
            return f"{masked_str[0:4]}-{masked_str[4:8]}-{masked_str[8:12]}-{masked_str[12:16]}"
        elif length == 15:
            return f"{masked_str[0:4]}-{masked_str[4:10]}-{masked_str[10:15]}"

        return masked_str

    @staticmethod
    def mask_account_number(account_number: str) -> str:
        """계좌번호 마스킹 (하이픈 포함)
        - 뒤에서부터 5자리 마스킹

        Args:
            account_number (str): _description_

        Returns:
            str: _description_
        """
        if not account_number or not account_number.strip():
            return ""

        # 자바의 toCharArray()와 대응
        chars = list(account_number)

        masked_count = 0

        # 뒤에서부터 순회 (range의 역순 활용)
        # len(chars) - 1부터 0까지 -1씩 감소
        for i in range(len(chars) - 1, -1, -1):
            if chars[i].isdigit():
                chars[i] = "*"
                masked_count += 1

            if masked_count == 5:
                break

        return "".join(chars)

    @staticmethod
    def mask_birthdate(birthdate: str) -> str:
        """생년월일 마스킹
        - 년도 마스킹

        Args:
            birthdate (str): _description_

        Returns:
            str: _description_
        """
        if not birthdate or not birthdate.strip():
            return ""

        has_hyphen = "-" in birthdate

        digits_only = re.sub("[^\\d]", "", birthdate)

        if len(digits_only) == 8:
            year_masked = "****"
            month = digits_only[4:6]
            day = digits_only[6:8]

            if has_hyphen:
                return f"{year_masked}-{month}-{day}"
            else:
                return f"{year_masked}{month}{day}"
        else:
            return ""

    @staticmethod
    def mask_ip_address(ip_address: str) -> str:
        """IP 주소 마스킹
        - 뒤 3자리 마스킹

        Args:
            ip_address (str): _description_

        Returns:
            str: _description_
        """
        if not ip_address or not ip_address.strip():
            return ""

        if re.match("\\d+\\.\\d+\\.\\d+\\.\\d+", ip_address):
            last_dot_index = ip_address.rfind(".")
            if last_dot_index != -1:
                prefix = ip_address[: last_dot_index + 1]
                return prefix + "***"

        return ""

    @staticmethod
    def mask_ipv6_address(ipv6_address: str) -> str:
        """IPv6 주소 마스킹
        - 뒤 2개 블록 마스킹

        Args:
            ipv6_address (str): _description_

        Returns:
            str: _description_
        """
        if not ipv6_address or not ipv6_address.strip():
            return ""

        # Scope ID 제거
        clean_address = ipv6_address.split("%")[0]

        try:
            # 유효한 IP 주소인지 검증
            ipaddress.IPv6Address(clean_address)

            return re.sub(r"(:[0-9a-fA-F]{1,4}){2}$", ":****:****", clean_address)
        except ValueError:
            return ""

    @staticmethod
    def mask_student_id(student_id: str) -> str:
        """학번 마스킹
        - 숫자 : 입학 연도 외 마스킹
        - 문자 + 숫자 : 문자만 마스킹

        Args:
            student_id (str): _description_

        Returns:
            str: _description_
        """
        if not student_id or not student_id.strip():
            return ""

        if re.match("\\d{8,9}", student_id):
            return student_id[:4] + "****"
        elif re.match("\\d{2}[A-Za-z]{2}\\d{4}", student_id):
            return student_id[:2] + "**" + student_id[4:8]

        return ""

    @staticmethod
    def mask_password(password: str) -> str:
        """비밀번호 마스킹
        - 계정 비밀번호는 대상 아님

        Args:
            password (str): _description_

        Returns:
            str: _description_
        """
        if not password or not password.strip():
            return ""

        return "*" * len(password)
