import logging


logger = logging.getLogger(__name__)


class ObjectUtil:
    is_null = "{} is null"
    is_null_or_empty = "{} is null or empty"

    @classmethod
    def is_blank(cls, obj: object, field_name: str) -> bool:
        """클래스의 Field가 Blank인지 체크

        Args:
            obj (object): _description_
            field_name (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not obj:
            raise ValueError(cls.is_null("obj"))

        if not field_name or not field_name.strip():
            raise ValueError(cls.is_null_or_empty.format("json_str"))

        value = getattr(obj, field_name, None)

        if value is None:
            return True

        if isinstance(value, str):
            return value.strip() == ""

        return False

    @classmethod
    def get_field_names(cls, obj: object) -> list:
        """클래스의 Field명 추출

        Args:
            obj (object): _description_

        Raises:
            ValueError: _description_

        Returns:
            list: _description_
        """
        if not obj:
            raise ValueError(cls.is_null("obj"))

        return list(vars(obj).keys())

    @classmethod
    def map_to_object(cls, map: dict, obj: object) -> None:
        """딕셔너리를 클래스로 변환

        Args:
            map (dict): _description_
            obj (object): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
        """
        if not map:
            raise ValueError(cls.is_null("map"))

        if not obj:
            raise ValueError(cls.is_null("obj"))

        for key, value in map.items():
            setattr(obj, key, value)

    @classmethod
    def get_byte_length(cls, obj: object, encoding: str) -> int:
        """클래스의 필드 변수 길이 구함

        Args:
            obj (object): _description_
            encoding (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            int: _description_
        """
        if not obj:
            raise ValueError(cls.is_null("obj"))

        if not encoding or not encoding.strip():
            raise ValueError(cls.is_null_or_empty.format("encoding"))

        byte_len = 0

        try:
            fields = vars(obj)

            for attr_name in fields:
                value = getattr(obj, attr_name)

                if value is not None:
                    s_value = str(value)
                    byte_len += len(s_value.encode(encoding))
        except (AttributeError, UnicodeEncodeError) as e:
            logger.error(f"Error calculating byte length: {e}")

        return byte_len

    @classmethod
    def get_byte_length_except(
        cls, obj: object, exclude_field: str, encoding: str
    ) -> int:
        """클래스의 필드 변수 길이 구함
        - 해당 필드를 제외한 길이 구함

        Args:
            obj (object): _description_
            exclude_field (str): _description_
            encoding (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            int: _description_
        """
        if not obj:
            raise ValueError(cls.is_null("obj"))

        if not exclude_field or not exclude_field.strip():
            raise ValueError(cls.is_null_or_empty.format("exclude_field"))

        if not encoding or not encoding.strip():
            raise ValueError(cls.is_null_or_empty.format("encoding"))

        byte_len = 0

        try:
            fields = vars(obj)

            for attr_name in fields:
                value = getattr(obj, attr_name)

                if attr_name != exclude_field and value is not None:
                    s_value = str(value)
                    byte_len += len(s_value.encode(encoding))
        except (AttributeError, UnicodeEncodeError) as e:
            logger.error(f"Error calculating byte length: {e}")

        return byte_len
