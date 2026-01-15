from datetime import datetime
from dateutil.relativedelta import relativedelta


class AgeUtil:
    """
    만나이, 한국식 나이, 보험 나이 등을 계산하는 기능 제공

    Author: 김대광
    """

    is_null_or_empty = "{} is null or empty"

    @classmethod
    def get_age(cls, birth_day: str, fix_day: str | None = None) -> int:
        """현재일을 기준으로 만나이 계산
        - fix_day가 있으면 기준일을 기준

        Args:
            birth_day (str): _description_
            fix_day (str | None, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if not birth_day or not birth_day.strip():
            raise ValueError(cls.is_null_or_empty.format("birth_day"))

        formatter = "%Y%m%d"

        birth = datetime.strptime(birth_day, formatter)

        if fix_day:
            now = datetime.strptime(fix_day, formatter)
        else:
            now = datetime.now()

        age = now.year - birth.year

        if (now.month, now.day) < (birth.month, birth.day):
            age -= 1

        return age

    @classmethod
    def get_korean_age(cls, birth_day: str, fix_day: str | None = None) -> int:
        """현재일을 기준으로 한국 나이 계산
        - fix_day가 있으면 기준일을 기준

        Args:
            birth_day (str): _description_
            fix_day (str | None, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if not birth_day or not birth_day.strip():
            raise ValueError(cls.is_null_or_empty.format("birth_day"))

        formatter = "%Y%m%d"

        birth = datetime.strptime(birth_day, formatter)

        if fix_day:
            now = datetime.strptime(fix_day, formatter)
        else:
            now = datetime.now()

        return now.year - birth.year + 1

    @classmethod
    def get_insur_age(cls, birth_day: str, fix_day: str | None = None) -> int:
        """현재일을 기준으로 보험나이 계
        - fix_day가 있으면 기준일을 기준

        Args:
            birth_day (str): _description_
            fix_day (str | None, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_

        Returns:
            int: _description_
        """
        if not birth_day or not birth_day.strip():
            raise ValueError(cls.is_null_or_empty.format("birth_day"))

        formatter = "%Y%m%d"

        birth = datetime.strptime(birth_day, formatter).date()

        if fix_day:
            now = datetime.strptime(fix_day, formatter).date()
        else:
            now = datetime.now().date()

        target_date = now - relativedelta(months=6)

        # 두 날짜 사이의 연도, 월, 일 차이를 정확히 계산 (Java의 ChronoUnit.YEARS.between 대응)
        diff = relativedelta(target_date, birth)

        return diff.years
