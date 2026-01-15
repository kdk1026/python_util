class UserAgentUtil:
    """
    Author: 김대광
    """

    is_null = "{} is null"
    is_null_or_empty = "{} is null or empty"

    @classmethod
    def is_check_user_agent(cls, ua_string: str, chk_str: str) -> bool:
        """UserAgent 에서 특정 문자열 유무 체크

        Args:
            ua_string (str): _description_
            chk_str (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not ua_string or not ua_string.strip():
            raise ValueError(cls.is_null_or_empty.format("ua_string"))

        if not chk_str or not chk_str.strip():
            raise ValueError(cls.is_null_or_empty.format("chk_str"))

        return chk_str in ua_string
