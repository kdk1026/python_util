import bcrypt


class BcryptUtil:
    """
    Author: 김대광
    """

    ORIGINAL_TEXT_IS_NULL = (
        "원본 텍스트가 비어 있거나 null입니다. 해싱을 수행할 수 없습니다."
    )

    @staticmethod
    def bcrypt_hash(original_text: str) -> str:
        """Bcrypt 해싱

        Args:
            original_text (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not original_text or not original_text.strip():
            raise ValueError(BcryptUtil.ORIGINAL_TEXT_IS_NULL)

        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(original_text.encode("utf-8"), salt)

        return hashed.decode("utf-8")

    @staticmethod
    def check_bcrypt_hash(original_text: str, hashed_text: str) -> bool:
        """Bcrypt 해싱 검증

        Args:
            original_text (str): _description_
            hashed_text (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not original_text or not original_text.strip():
            raise ValueError(BcryptUtil.ORIGINAL_TEXT_IS_NULL)

        if not hashed_text or not hashed_text.strip():
            raise ValueError(
                "해시된 텍스트가 비어 있거나 null입니다. 검증을 수행할 수 없습니다."
            )

        return bcrypt.checkpw(
            original_text.encode("utf-8"), hashed_text.encode("utf-8")
        )
