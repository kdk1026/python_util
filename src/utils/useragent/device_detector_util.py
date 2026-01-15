from functools import lru_cache
from device_detector import DeviceDetector


class DeviceDetectorUtil:
    """
    User Agent 문자열의 형식은 언제든지 바뀔 수 있으므로 라이브러리를 이용하면

    라이브러리 제작사에게 맡기고 최신 버전으로 업데이트만 처리

    Author: 김대광
    """

    _is_null = "{} is null"
    _is_null_or_empty = "{} is null or empty"

    @staticmethod
    @lru_cache(maxsize=10000)
    def _get_parsed_result(ua_string: str) -> DeviceDetector:
        return DeviceDetector(ua_string).parse()

    @classmethod
    def parse(cls, ua_string: str) -> dict:
        """User-Agent 문자열을 분석하여 주요 정보를 반환

        Args:
            ua_string (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            dict: _description_
        """
        if not ua_string or not ua_string.strip():
            raise ValueError(cls._is_null_or_empty.format("ua_string"))

        result = cls._get_parsed_result(ua_string)

        result = {
            # 기기 분류 (Desktop, smartphone, tablet, tv, etc.)
            "DeviceClass": result.device_type(),
            # 기기 명칭 (Brand + Model)
            "DeviceName": f"{result.device_brand()} {result.device_model()}".strip(),
            # 브라우저 이름 (Chrome, Safari, etc.)
            "AgentName": result.client_name(),
            # 브라우저 버전
            "AgentVersion": result.client_version(),
            # 운영체제 이름 (Windows, Android, iOS, etc.)
            "OperatingSystemName": result.os_name(),
            # 운영체제 버전
            "OperatingSystemVersion": result.os_version(),
        }

        return result

    @classmethod
    def get_field(cls, ua_string: str, field_name: str) -> str:
        """특정 필드 하나만 반환

        Args:
            ua_string (str): _description_
            field_name (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not ua_string or not ua_string.strip():
            raise ValueError(cls._is_null_or_empty.format("ua_string"))

        if not field_name or not field_name.strip():
            raise ValueError(cls._is_null_or_empty.format("field_name"))

        result = cls._get_parsed_result(ua_string)

        if field_name == "DeviceName":
            return result.device_model()
        elif field_name == "Brand":
            return result.device_brand_name()
        elif field_name == "OS":
            return result.os_name()
        elif field_name == "Browser":
            return result.client_name()

        return getattr(result, field_name, lambda: "Unknown")()
