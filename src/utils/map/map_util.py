class MapUtil:
    is_null = "{} is null"
    is_null_or_empty = "{} is null or empty"

    @classmethod
    def object_to_map(cls, obj: object) -> dict:
        """클래스를 딕셔너리로 변환

        Args:
            obj (object): _description_

        Raises:
            ValueError: _description_

        Returns:
            dict: _description_
        """
        if not obj:
            raise ValueError(cls.is_null("obj"))

        return obj.__dict__

    @classmethod
    def is_blank(cls, map: dict, key: str) -> bool:
        """dict의 Key가 Blank인지 체크

        Args:
            map (dict): _description_
            key (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not map:
            raise ValueError(cls.is_null("map"))

        if not key or not key.strip():
            raise ValueError(cls.is_null_or_empty.format("key"))

        if not map.get(key):
            return True
        else:
            return not map.get(key).strip()

    @classmethod
    def not_contains_key_to_blank(cls, map: dict, *keys: str) -> None:
        """dict에 Key가 없으면 Blank 처리

        Args:
            map (dict): _description_
            key (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
        """
        if not map:
            raise ValueError(cls.is_null("map"))

        if not keys:
            raise ValueError(cls.is_null_or_empty.format("keys"))

        for key in keys:
            map.setdefault(key, "")

    @classmethod
    def null_to_blank(cls, map: dict) -> None:
        """None을 Blank 처리

        Args:
            map (dict): _description_

        Raises:
            ValueError: _description_

        Returns:
            dict: _description_
        """
        if not map:
            raise ValueError(cls.is_null("map"))

        for key, value in map.items():
            if value is None:
                map[key] = ""

    @classmethod
    def space_to_blank(cls, map: dict) -> dict:
        """Space를 Blank 처리

        Args:
            map (dict): _description_
            key (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            dict: _description_
        """
        if not map:
            raise ValueError(cls.is_null("map"))

        return {k: ("" if v == " " else v) for k, v in map.items()}
