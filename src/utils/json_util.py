import json
import logging
import os

logger = logging.getLogger(__name__)


class JsonUtil:
    """
    Author: 김대광
    """

    is_null = "{} is null"
    is_null_or_empty = "{} is null or empty"

    @classmethod
    def to_json(cls, obj: object | dict | list, is_pretty: bool = False) -> str:
        """클래스, 딕셔너리, 리스트를 JSON 문자열로 변환

        Args:
            obj (object | dict | list): _description_
            is_pretty (bool, optional): _description_. Defaults to False.

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not obj:
            raise ValueError(cls.is_null("obj"))

        if isinstance(obj, dict) or isinstance(obj, list):
            return json.dumps(obj, ensure_ascii=False, indent=4 if is_pretty else None)
        else:
            return json.dumps(
                obj.__dict__, ensure_ascii=False, indent=4 if is_pretty else None
            )

    @classmethod
    def from_json(cls, json_str: str) -> dict | list:
        """JSON 문자열을 딕셔너리, 리스트로 변환

        Args:
            json_str (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            dict | list: _description_
        """
        if not json_str or not json_str.strip():
            raise ValueError(cls.is_null_or_empty.format("json_str"))

        return json.loads(json_str)

    @classmethod
    def read_json_file(cls, file_path: str) -> dict | list:
        """JSON 파일을 읽어서 딕셔너리, 리스트로 변환

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            dict | list: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls.is_null_or_empty.format("file_path"))

        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"JSON 형식이 잘못되었습니다: {e}")
        else:
            logger.error(f"Error: File not found at {file_path}")
