import logging
import requests

logger = logging.getLogger(__name__)


class RequestsUtil:
    """
    is_ssl은 False로 해서 오류 나는 경우에만 True로 사용

    response = requests.post(url, json=payload)
        : json 파라미터를 사용하면 자동으로 Content-Type: application/json 설정
        : data 파라미터를 사용하면 자동으로 Content-Type: application/x-www-form-urlencoded 설정
        : file 파라미터를 사용하면 자동으로 Content-Type: multipart/form-data 설정
        : 그 외에는 헤더에 직접 설정
    """

    is_null = "{} is null"
    is_null_or_empty = "{} is null or empty"

    @classmethod
    def get(cls, is_ssl: bool, url: str = "", header_map: dict = None) -> dict | None:
        """HttpClient GET 요청

        Args:
            is_ssl (bool): _description_
            url (str, optional): _description_. Defaults to "".
            header_map (dict, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_

        Returns:
            dict | None: _description_
        """
        if not url or not url.strip():
            raise ValueError(cls.is_null_or_empty.format("url"))

        if is_ssl:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            response = requests.get(
                url, headers=header_map or {}, verify=True if is_ssl == False else False
            )

            if not response.ok:
                logger.warning(f"Status Code: {response.status_code}")
                return None

            try:
                return response.json()
            except ValueError:
                return {"text": response.text}
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request Error: {e}")
            return None

    @classmethod
    def post(
        cls,
        is_ssl: bool,
        url: str = "",
        header_map: dict = None,
        body_map: dict = None,
        is_type: int = 1,
    ) -> dict | None:
        """HttpClient POST 요청
        - is_type = 1 (json)
        - is_type = 2 (data = form)
        - is_type = 3 (file)

        Args:
            is_ssl (bool): _description_
            url (str, optional): _description_. Defaults to "".
            header_map (dict, optional): _description_. Defaults to None.
            body_map (dict, optional): _description_. Defaults to None.
            is_type (int, optional): _description_. Defaults to 1.

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            dict | None: _description_
        """
        if not url or not url.strip():
            raise ValueError(cls.is_null_or_empty.format("url"))

        type_mapping = {1: "json", 2: "data", 3: "files"}
        param_name = type_mapping.get(is_type)

        if not param_name:
            raise ValueError(f"Invalid is_type: {is_type}. Choose 1, 2, or 3.")

        if is_ssl:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            response = requests.post(
                url,
                headers=header_map or {},
                verify=True if is_ssl == False else False,
                **{param_name: body_map or {}},
            )

            if not response.ok:
                logger.warning(f"Status Code: {response.status_code}")
                return None

            try:
                return response.json()
            except ValueError:
                return {"text": response.text}
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request Error: {e}")
            return None
