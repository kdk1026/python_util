from typing import Any
import logging

logger = logging.getLogger(__name__)


class ByteUtils:
    """
    Author: 김대광
    """

    @staticmethod
    def get_byte_length(obj: Any, encoding: str = "utf-8") -> int:
        """객체의 bytes 길이 구하기

        Args:
            obj (Any): _description_
            encoding (str, optional): _description_. Defaults to "utf-8".

        Returns:
            int: _description_
        """
        encoding = (encoding or "utf-8").strip()

        if obj is None:
            return 0

        byte_len = 0

        try:
            attrs = vars(obj)

            for val in attrs.values():
                if val is not None:
                    byte_len += len(str(val).encode(encoding))
        except LookupError:
            logger.error(f"지원되지 않는 인코딩입니다: {encoding}")
        except (AttributeError, TypeError) as e:
            logger.error(f"객체 속성 접근 중 오류 발생: {e}")
        except Exception as e:
            logger.error(f"알 수 없는 오류 발생: {e}", exc_info=True)

        return byte_len

    @staticmethod
    def get_dict_byte_length(data_map: dict, encoding: str = "utf-8") -> int:
        """딕셔너리(dictionary) 자료형의 bytes 길이 구하기

        Args:
            data_map (dict): _description_
            encoding (str, optional): _description_. Defaults to "utf-8".

        Returns:
            int: _description_
        """
        encoding = (encoding or "utf-8").strip()

        if not data_map:
            return 0

        byte_len = 0

        try:
            for val in data_map.values():
                if val is not None:
                    byte_len += len(str(val).encode(encoding))
        except LookupError:
            logger.error(f"지원되지 않는 인코딩입니다: {encoding}")
        except Exception as e:
            logger.error(f"알 수 없는 오류 발생: {e}", exc_info=True)

        return byte_len
