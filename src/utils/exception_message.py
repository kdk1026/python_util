class ExceptionMessage:
    """
    Author: 김대광
    """

    @staticmethod
    def is_null(param_name: str) -> str:
        return "{} is null".format(param_name)

    @staticmethod
    def in_valid(param_name: str) -> str:
        return "{} is inValid".format(param_name)

    @staticmethod
    def is_null_or_empty(param_name: str) -> str:
        return "{} is null or empty".format(param_name)

    @staticmethod
    def is_negative(param_name: str) -> str:
        return "{} is negative".format(param_name)
