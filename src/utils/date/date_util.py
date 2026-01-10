import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from babel.dates import format_date


class DateUtil:
    """
    (포맷) %Y-%m-%d %H:%M:%S = yyyy-MM-dd HH:mm:ss
    """

    class Today:
        """
        현재 날짜 및 시간 반환
        """

        @staticmethod
        def get_today_string() -> str:
            """현재 날짜를 yyyyMMdd 형식의 String 타입으로 반환

            Returns:
                str: _description_
            """
            return datetime.now().strftime("%Y%m%d")

        @staticmethod
        def get_today_string_formatted(date_format: str) -> str:
            """현재 날짜를 해당 포맷의 String 타입로 반환

            Args:
                date_format (str): _description_

            Returns:
                str: _description_
            """
            return datetime.now().strftime(date_format)

        @staticmethod
        def get_current_time() -> str:
            """현재 시간을 HHmmss 형식의 String 타입으로 반환

            Returns:
                str: _description_
            """
            return datetime.now().strftime("%H%M%S")

        @staticmethod
        def get_year() -> int:
            """현재 연도 반환

            Returns:
                _type_: _description_
            """
            return datetime.now().year

        @staticmethod
        def get_month() -> int:
            """현재 월 반환

            Returns:
                _type_: _description_
            """
            return datetime.now().month

        @staticmethod
        def get_day_of_month() -> int:
            """현재 일 반환

            Returns:
                _type_: _description_
            """
            return datetime.now().day

        @staticmethod
        def get_hour() -> int:
            """현재 시간 반환

            Returns:
                _type_: _description_
            """
            return datetime.now().hour

        @staticmethod
        def get_minute() -> int:
            """현재 분 반환

            Returns:
                _type_: _description_
            """
            return datetime.now().minute

    class StringFormat:
        """
        String 타입 형식의 포맷 변환
        """

        @staticmethod
        def get_string_date(str_date: str, date_format: str) -> str:
            """yyyyMMdd 형식의 String 타입을 해당 포맷의 String 타입으로 반환

            Args:
                str_date (str): _description_
                date_format (str): _description_

            Returns:
                str: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d")
            return date.strftime(date_format)

        @staticmethod
        def get_string_date_time(str_date: str, date_format: str) -> str:
            """yyyyMMddHHmmss 형식의 String 타입을 해당 포맷의 String 타입으로 반환

            Args:
                str_date (str): _description_
                date_format (str): _description_

            Returns:
                str: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d%H%M%S")
            return date.strftime(date_format)

    class Convert:
        """
        타입 변환
        """

        @staticmethod
        def get_string_to_date(str_date: str) -> datetime:
            """yyyyMMdd(HHmmss) 형식의 String 타입을 datetime 타입으로 반환

            Args:
                str_date (str): _description_

            Returns:
                datetime: _description_
            """
            if len(str_date) == 14:
                return datetime.strptime(str_date, "%Y%m%d%H%M%S")
            else:
                return datetime.strptime(str_date, "%Y%m%d")

        @staticmethod
        def get_date_to_string(date: datetime) -> str:
            """datetime 타입 객체를 yyyyMMdd 형식의 String 타입으로 반환

            Args:
                date (datetime): _description_

            Returns:
                str: _description_
            """
            return date.strftime("%Y%m%d")

        @staticmethod
        def get_date_to_formatted_string(date: datetime, date_format: str) -> str:
            """datetime 타입 객체를 해당 포맷의 String 타입으로 반환

            Args:
                date (datetime): _description_
                date_format (str): _description_

            Returns:
                str: _description_
            """
            return date.strftime(date_format)

    class CalcDate:
        """
        이전/이후 날짜 반환
        """

        @staticmethod
        def plus_minus_day(days: int) -> str:
            """현재 날짜의 이전/이후 날짜를 yyyyMMdd 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 날짜 반환
            - 인자 값이 양수 인 경우, 이후 날짜 반환

            Args:
                days (int): _description_

            Returns:
                str: _description_
            """
            now = datetime.now()

            if days > 0:
                return (now + timedelta(days=days)).strftime("%Y%m%d")
            else:
                return (now - timedelta(days=(days * -1))).strftime("%Y%m%d")

        @staticmethod
        def plus_minus_day_from(str_date: str, days: int) -> str:
            """yyyyMMdd 형식의 String 타입 날짜의 이전/이후 날짜를 yyyyMMdd 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 날짜 반환
            - 인자 값이 양수 인 경우, 이후 날짜 반환

            Args:
                str_date (str): _description_
                days (int): _description_

            Returns:
                str: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d")

            if days > 0:
                return (date + timedelta(days=days)).strftime("%Y%m%d")
            else:
                return (date - timedelta(days=(days * -1))).strftime("%Y%m%d")

        @staticmethod
        def plus_minus_month(months: int) -> str:
            """현재 날짜의 이전/이후 날짜를 yyyyMMdd 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 날짜 반환
            - 인자 값이 양수 인 경우, 이후 날짜 반환

            Args:
                months (int): _description_

            Returns:
                str: _description_
            """
            now = datetime.now()

            if months > 0:
                return (now + relativedelta(months=months)).strftime("%Y%m%d")
            else:
                return (now - relativedelta(months=(months * -1))).strftime("%Y%m%d")

        @staticmethod
        def plus_minus_month_formatted(months: int, date_format: str) -> str:
            """현재 날짜의 이전/이후 날짜를 해당 포맷 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 날짜 반환
            - 인자 값이 양수 인 경우, 이후 날짜 반환

            Args:
                months (int): _description_
                date_format (str): _description_

            Returns:
                str: _description_
            """
            now = datetime.now()

            if months > 0:
                return (now + relativedelta(months=months)).strftime(date_format)
            else:
                return (now - relativedelta(months=(months * -1))).strftime(date_format)

        @staticmethod
        def plus_minus_month_from(str_date: str, months: int) -> str:
            """yyyyMMdd 형식의 String 타입 날짜의 이전/이후 날짜를 yyyyMMdd 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 날짜 반환
            - 인자 값이 양수 인 경우, 이후 날짜 반환

            Args:
                str_date (str): _description_
                months (int): _description_

            Returns:
                str: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d")

            if months > 0:
                return (date + relativedelta(months=months)).strftime("%Y%m%d")
            else:
                return (date - relativedelta(months=(months * -1))).strftime("%Y%m%d")

        @staticmethod
        def plus_minus_month_from_formatted(
            str_date: str, months: int, date_format: str
        ) -> str:
            """헤딩 포멧 형식의 String 타입 날짜의 이전/이후 날짜를 헤딩 포멧 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 날짜 반환
            - 인자 값이 양수 인 경우, 이후 날짜 반환

            Args:
                str_date (str): _description_
                months (int): _description_
                date_format (str): _description_

            Returns:
                str: _description_
            """
            date = datetime.strptime(str_date, date_format)

            if months > 0:
                return (date + relativedelta(months=months)).strftime(date_format)
            else:
                return (date - relativedelta(months=(months * -1))).strftime(
                    date_format
                )

        @staticmethod
        def plus_minus_year(years: int) -> str:
            """현재 날짜의 이전/이후 날짜를 yyyyMMdd 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 날짜 반환
            - 인자 값이 양수 인 경우, 이후 날짜 반환

            Args:
                years (int): _description_

            Returns:
                str: _description_
            """
            now = datetime.now()

            if years > 0:
                return (now + relativedelta(years=years)).strftime("%Y%m%d")
            else:
                return (now - relativedelta(years=(years * -1))).strftime("%Y%m%d")

        @staticmethod
        def plus_minus_year_formatted(years: int, date_format: str) -> str:
            """현재 날짜의 이전/이후 날짜를 해당 포맷 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 날짜 반환
            - 인자 값이 양수 인 경우, 이후 날짜 반환

            Args:
                years (int): _description_
                date_format (str): _description_

            Returns:
                str: _description_
            """
            now = datetime.now()

            if years > 0:
                return (now + relativedelta(years=years)).strftime(date_format)
            else:
                return (now - relativedelta(years=(years * -1))).strftime(date_format)

        @staticmethod
        def plus_minus_year_from(str_date: str, years: int) -> str:
            """yyyyMMdd 형식의 String 타입 날짜의 이전/이후 날짜를 yyyyMMdd 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 날짜 반환
            - 인자 값이 양수 인 경우, 이후 날짜 반환

            Args:
                str_date (str): _description_
                years (int): _description_

            Returns:
                str: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d")

            if years > 0:
                return (date + relativedelta(years=years)).strftime("%Y%m%d")
            else:
                return (date - relativedelta(years=(years * -1))).strftime("%Y%m%d")

        @staticmethod
        def plus_minus_year_from_formatted(
            str_date: str, years: int, date_format: str
        ) -> str:
            """헤딩 포멧 형식의 String 타입 날짜의 이전/이후 날짜를 헤딩 포멧 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 날짜 반환
            - 인자 값이 양수 인 경우, 이후 날짜 반환

            Args:
                str_date (str): _description_
                years (int): _description_
                date_format (str): _description_

            Returns:
                str: _description_
            """
            date = datetime.strptime(str_date, date_format)

            if years > 0:
                return (date + relativedelta(years=years)).strftime(date_format)
            else:
                return (date - relativedelta(years=(years * -1))).strftime(date_format)

    class CalcTime:
        """
        이전/이후 시간각반환
        """

        @staticmethod
        def plus_minus_hour(hours: int) -> str:
            """현재 날짜의 이전/이후 날짜를 yyyyMMddHHmmss 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 시간 반환
            - 인자 값이 양수 인 경우, 이후 시간 반환

            Args:
                hours (int): _description_

            Returns:
                str: _description_
            """
            now = datetime.now()

            if hours > 0:
                return (now + timedelta(hours=hours)).strftime("%Y%m%d%H%M%S")
            else:
                return (now - timedelta(hours=(hours * -1))).strftime("%Y%m%d%H%M%S")

        @staticmethod
        def plus_minus_hour_from(str_date: str, hours: int) -> str:
            """yyyyMMddHHmmss 형식의 String 타입 날짜의 이전/이후 날짜를 yyyyMMddHHmmss 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 시간 반환
            - 인자 값이 양수 인 경우, 이후 시간 반환

            Args:
                str_date (str): _description_
                hours (int): _description_

            Returns:
                str: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d%H%M%S")

            if hours > 0:
                return (date + timedelta(hours=hours)).strftime("%Y%m%d%H%M%S")
            else:
                return (date - timedelta(hours=(hours * -1))).strftime("%Y%m%d%H%M%S")

        @staticmethod
        def plus_minus_minute(minutes: int) -> str:
            """현재 날짜의 이전/이후 날짜를 yyyyMMddHHmmss 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 시간 반환
            - 인자 값이 양수 인 경우, 이후 시간 반환

            Args:
                minutes (int): _description_

            Returns:
                str: _description_
            """
            now = datetime.now()

            if minutes > 0:
                return (now + timedelta(minutes=minutes)).strftime("%Y%m%d%H%M%S")
            else:
                return (now - timedelta(minutes=(minutes * -1))).strftime(
                    "%Y%m%d%H%M%S"
                )

        @staticmethod
        def plus_minus_minute_from(str_date: str, minutes: int) -> str:
            """yyyyMMddHHmmss 형식의 String 타입 날짜의 이전/이후 날짜를 yyyyMMddHHmmss 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 시간 반환
            - 인자 값이 양수 인 경우, 이후 시간 반환

            Args:
                str_date (str): _description_
                minutes (int): _description_

            Returns:
                str: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d%H%M%S")

            if minutes > 0:
                return (date + timedelta(minutes=minutes)).strftime("%Y%m%d%H%M%S")
            else:
                return (date - timedelta(minutes=(minutes * -1))).strftime(
                    "%Y%m%d%H%M%S"
                )

        @staticmethod
        def plus_minus_second(seconds: int) -> str:
            """현재 날짜의 이전/이후 날짜를 yyyyMMddHHmmss 형식의 String 타입으로 반환
            - 인자 값이 음수 인 경우, 이전 시간 반환
            - 인자 값이 양수 인 경우, 이후 시간 반환

            Args:
                seconds (int): _description_

            Returns:
                str: _description_
            """
            now = datetime.now()

            if seconds > 0:
                return (now + timedelta(seconds=seconds)).strftime("%Y%m%d%H%M%S")
            else:
                return (now - timedelta(seconds=(seconds * -1))).strftime(
                    "%Y%m%d%H%M%S"
                )

    class GetDateInterval:
        """
        기간 간격 구하기
        """

        @staticmethod
        def interval_years(str_fix_date: str) -> int:
            """현재 날짜와 년 간격 구하기
            - 0:같다, 양수:크다, 음수:작다

            Args:
                str_fix_date (str): _description_

            Returns:
                int: _description_
            """
            fix_date = datetime.strptime(str_fix_date, "%Y%m%d")
            target_date = datetime.now()

            diff = relativedelta(fix_date, target_date)
            return diff.years

        @staticmethod
        def interval_months(str_fix_date: str) -> int:
            """현재 날짜와 월 간격 구하기
            - 0:같다, 양수:크다, 음수:작다

            Args:
                str_fix_date (str): _description_

            Returns:
                int: _description_
            """
            fix_date = datetime.strptime(str_fix_date, "%Y%m%d")
            target_date = datetime.now()

            diff = relativedelta(fix_date, target_date)
            return diff.months

        @staticmethod
        def interval_days(str_fix_date: str) -> int:
            """현재 날짜와 일 간격 구하기
            - 0:같다, 양수:크다, 음수:작다

            Args:
                str_fix_date (str): _description_

            Returns:
                int: _description_
            """
            fix_date = datetime.strptime(str_fix_date, "%Y%m%d")
            target_date = datetime.now()

            diff = relativedelta(fix_date, target_date)
            return diff.days

    class GetTimeInterval:
        """
        시간 간격 구하기
        """

        @staticmethod
        def interval_hours(str_fix_date: str) -> int:
            """현재 날짜와 시간 간격 구하기
            - 0:같다, 양수:크다, 음수:작다

            Args:
                str_fix_date (str): _description_

            Returns:
                int: _description_
            """
            fix_date = datetime.strptime(str_fix_date, "%Y%m%d%H%M%S")
            target_date = datetime.now()

            diff = relativedelta(fix_date, target_date)
            return diff.hours

        @staticmethod
        def interval_minutes(str_fix_date: str) -> int:
            """현재 날짜와 분 간격 구하기
            - 0:같다, 양수:크다, 음수:작다

            Args:
                str_fix_date (str): _description_

            Returns:
                int: _description_
            """
            fix_date = datetime.strptime(str_fix_date, "%Y%m%d%H%M%S")
            target_date = datetime.now()

            diff = relativedelta(fix_date, target_date)
            return diff.minutes

        @staticmethod
        def interval_seconds(str_fix_date: str) -> int:
            """현재 날짜와 초 간격 구하기
            - 0:같다, 양수:크다, 음수:작다

            Args:
                str_fix_date (str): _description_

            Returns:
                int: _description_
            """
            fix_date = datetime.strptime(str_fix_date, "%Y%m%d%H%M%S")
            target_date = datetime.now()

            diff = relativedelta(fix_date, target_date)
            return diff.seconds

    class GetDayOfWeek:
        """
        요일 구하기
        """

        @staticmethod
        def get_day_of_week() -> int:
            """현재 날짜의 요일 구하기

            Returns:
                _type_: _description_
            """
            return datetime.now().isoweekday()

        @staticmethod
        def get_day_of_week_from_date(str_date: str) -> int:
            """yyyyMMdd 형식의 String 타입 날짜의 요일 구하기

            Args:
                str_date (str): _description_

            Returns:
                int: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d")
            return date.now().isoweekday()

        @staticmethod
        def get_week_start_day() -> int:
            """현재 날짜의 1일의 요일 반환

            Returns:
                _type_: _description_
            """
            first_day_of_month = datetime.now().replace(day=1)
            return first_day_of_month.isoweekday()

        @staticmethod
        def get_week_start_day_from_date(str_date: str) -> int:
            """yyyyMMdd 형식의 String 타입에 해당하는 1일의 요일 반환

            Args:
                str_date (str): _description_

            Returns:
                int: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d")

            first_day_of_month = date.replace(day=1)
            return first_day_of_month.isoweekday()

        @staticmethod
        def get_today_day_of_week_locale(locale_code="ko_KR") -> str:
            """현재 날짜의 로케일 요일 구하기

            Args:
                locale_code (str, optional): _description_. Defaults to "ko_KR".

            Returns:
                _type_: _description_
            """
            now = datetime.now()
            return format_date(now, format="E", locale=locale_code)

        @staticmethod
        def get_day_of_week_from_date_locale(str_date: str, locale_code="ko_KR"):
            """yyyyMMdd 형식의 String 타입 날짜의 한글 요일 구하기

            Args:
                str_date (str): _description_
                locale_code (str, optional): _description_. Defaults to "ko_KR".

            Returns:
                _type_: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d")
            return format_date(date, format="E", locale=locale_code)

    class GetDayOfMonth:
        """
        마지막 일자 반환
        """

        @staticmethod
        def get_end_of_current_month() -> int:
            """현재 날짜의 마지막 일자를 반환

            Returns:
                _type_: _description_
            """
            now = datetime.now()
            return calendar.monthrange(now.year, now.month)[1]

        @staticmethod
        def get_end_of_current_month_string() -> str:
            """현재 날짜의 마지막 일자를 yyyyMMdd 형식으로 반환

            Returns:
                str: _description_
            """
            now = datetime.now()

            last_day = calendar.monthrange(now.year, now.month)[1]

            last_date_obj = now.replace(day=last_day)
            return last_date_obj.strftime("%Y%m%d")

        @staticmethod
        def get_end_of_month_from_date(str_date: str) -> int:
            """yyyyMMdd 형식의 String 타입에 해당하는 월의 마지막 일자를 반환

            Args:
                str_date (str): _description_

            Returns:
                int: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d")
            return calendar.monthrange(date.year, date.month)[1]

        @staticmethod
        def get_end_of_month_string_from_date(str_date: str) -> str:
            """yyyyMMdd 형식의 String 타입에 해당하는 월의 마지막 일자를 yyyyMMdd 형식으로 반환

            Args:
                str_date (str): _description_

            Returns:
                str: _description_
            """
            date = datetime.strptime(str_date, "%Y%m%d")

            last_day = calendar.monthrange(date.year, date.month)[1]

            last_date_obj = date.replace(day=last_day)
            return last_date_obj.strftime("%Y%m%d")

    class UnixTimestamp:
        """
        Unix Timestamp
        """

        @staticmethod
        def current_millis() -> int:
            """현재 시간을 밀리초 단위로 반환

            Returns:
                _type_: _description_
            """
            return int(datetime.now().timestamp() * 1000)

        @staticmethod
        def mills_to_datetime(mills) -> datetime:
            """밀리초를 datetime 객체로 변환

            Args:
                mills (_type_): _description_

            Returns:
                datetime: _description_
            """
            return datetime.fromtimestamp(mills / 1000.0)

        @classmethod
        def get_unix_timestamp(cls) -> int:
            """current Unix Timestamp
            - https://www.epochconverter.com/

            Returns:
                int: _description_
            """
            return cls.current_millis() / 1000

        @classmethod
        def timestamp_to_date_time(cls, timestamp: int) -> datetime:
            """timestamp to datetime

            Args:
                timestamp (int): _description_

            Returns:
                int: _description_
            """
            return cls.mills_to_datetime(timestamp * 1000)

    class Check:
        """
        Check
        """

        @staticmethod
        def is_last_week_of_month(date: datetime) -> bool:
            """해당 날짜가 월의 마지막에 속하는지 체크

            Args:
                date (datetime): _description_

            Returns:
                bool: _description_
            """
            # 해당 월의 마지막 날 구하기
            last_day_num = calendar.monthrange(date.year, date.month)[1]
            last_day_of_month = date.replace(day=last_day_num)

            # 마지막 일요일(Start of Last Week) 구하기
            days_to_subtract = (last_day_of_month.weekday() + 1) % 7
            start_of_last_week = last_day_of_month - timedelta(days=days_to_subtract)

            return date >= start_of_last_week

        @staticmethod
        def is_first_week_of_month(date: datetime) -> bool:
            """해당 날짜가 월의 첫째주에 속하는지 체크

            Args:
                date (datetime): _description_

            Returns:
                bool: _description_
            """
            # 해당 월의 첫 번째 날 구하기
            first_day_of_month = date.replace(day=1)

            # 첫 번째 일요일(End of First Week) 구하기
            days_to_add = (6 - first_day_of_month.weekday()) % 7
            end_of_first_week = first_day_of_month + timedelta(days=days_to_add)

            return date <= end_of_first_week
