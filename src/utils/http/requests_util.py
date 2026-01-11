import logging
import requests

logger = logging.getLogger(__name__)


class RequestsUtil:
    """
    is_ssl은 False로 해서 오류 나는 경우에만 True로 사용

    response = requests.post(url, json=payload)
        : json 파라미터를 사용하면 자동으로 Content-Type: application/json 설정
        : 그 외에는 헤더에 직접 설정
    """

    is_null = "{} is null"
    is_null_or_empty = "{} is null or empty"

    @classmethod
    def get(cls, is_ssl: bool, url: str = "", header_map: dict = {}) -> dict | None:
        """HttpClient GET 요청

        Args:
            is_ssl (bool): _description_
            url (str, optional): _description_. Defaults to "".
            header_map (dict, optional): _description_. Defaults to {}.

        Raises:
            ValueError: _description_

        Returns:
            dict | None: _description_
        """
        if not url or not url.strip():
            raise ValueError(cls.is_null_or_empty.format("url"))

        response = requests.get(
            url, headers=header_map, verify=True if is_ssl == False else False
        )

        if response.ok:
            return response.json()
        else:
            logger.warning(f"Status Code: {response.status_code}")
            return None

    @classmethod
    def post(
        cls,
        is_ssl: bool,
        url: str = "",
        header_map: dict = {},
        body_map: dict = {},
        is_json: bool = True,
    ) -> dict | None:
        """HttpClient POST 요청

        Args:
            is_ssl (bool): _description_
            url (str, optional): _description_. Defaults to "".
            header_map (dict, optional): _description_. Defaults to {}.
            body_map (dict, optional): _description_. Defaults to {}.
            is_json (bool, optional): _description_. Defaults to True.

        Raises:
            ValueError: _description_

        Returns:
            dict | None: _description_
        """
        if not url or not url.strip():
            raise ValueError(cls.is_null_or_empty.format("url"))

        if is_json:
            response = requests.post(
                url,
                headers=header_map,
                verify=True if is_ssl == False else False,
                json=body_map,
            )
        else:
            response = requests.post(
                url,
                headers=header_map,
                verify=True if is_ssl == False else False,
                data=body_map,
            )

        if response.ok:
            return response.json()
        else:
            logger.warning(f"Status Code: {response.status_code}")
            return None
