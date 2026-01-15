class CarriageReturnUtil:
    """
    Author: 김대광
    """

    __BR_TAG = "<br />"

    @classmethod
    def change_br_tag(cls, content: str) -> str | None:
        r"""캐리지 리턴 문자열을 줄바꿈 태그로 변환
        - \r\n = Windows
        - \r = 구형 Mac OS (9 이하)
        - \n = Unix/Linux/최신 Mac

        Args:
            content (str): _description_

        Returns:
            str | None: _description_
        """
        if not content or not content.strip():
            return None

        return (
            content.replace("\r\n", cls.__BR_TAG)
            .replace("\r", cls.__BR_TAG)
            .replace("\n", cls.__BR_TAG)
        )
