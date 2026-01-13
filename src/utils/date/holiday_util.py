from dataclasses import dataclass
import logging

import requests

logger = logging.getLogger(__name__)


class HolidayUtil:
    """
    www.data.go.kr
    : 한국천문연구원_특일 정보
    """

    __is_null_or_empty = "{} is null or empty"

    __API_URL = (
        "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    )

    @dataclass
    class HolidayData:
        date_kind: str
        date_name: str
        is_holiday: str
        locdate: str
        seq: str

        @classmethod
        def from_dict(cls, data: dict):
            return cls(
                date_kind=data.get("dateKind"),
                date_name=data.get("dateName"),
                is_holiday=data.get("isHoliday"),
                locdate=data.get("locdate"),
                seq=str(data.get("seq", "")),
            )

    @classmethod
    def get_holiday_list(
        cls, service_decoding_key: str, year: int, month: int | None = None
    ) -> list | None:
        if not service_decoding_key or not service_decoding_key.strip():
            raise ValueError(cls.__is_null_or_empty.format("service_decoding_key"))

        if year < 1900 or year > 2100:
            raise ValueError("연도는 1900년에서 2100년 사이여야 합니다.")

        params = {
            "serviceKey": service_decoding_key,
            "solYear": year,
            "_type": "json",
        }

        if month is not None:
            if month < 1 or month > 12:
                raise ValueError(f"월은 1~12 사이여야 합니다: {month}")

            params["solMonth"] = f"{month:02d}"

        try:
            response = requests.get(HolidayUtil.__API_URL, params=params)

            if not response.ok:
                logger.warning(f"Status Code: {response.status_code}")
                return None

            result_map: dict = response.json()

            items = (
                result_map.get("response", {})
                .get("body", {})
                .get("items", {})
                .get("item", [])
            )

            if not items:
                return None

            if isinstance(items, dict):
                items = [items]

            return [HolidayUtil.HolidayData.from_dict(item) for item in items]
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request Error: {e}")
            return None
