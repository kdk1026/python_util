import base64
import logging

logger = logging.getLogger(__name__)


class Base64Util:
    __is_null_or_empty = "{} is null or empty"

    @classmethod
    def encode(cls, text: str, charset: str | None = "utf-8") -> str | None:
        if not text or not text.strip():
            raise ValueError(cls.__is_null_or_empty.format("str"))

        try:
            raw_bytes = text.encode(charset)

            encoded_bytes = base64.b64encode(raw_bytes)

            # 결과는 항상 ASCII 범위이므로 utf-8로 안전하게 문자열 변환
            return encoded_bytes.decode("utf-8")
        except LookupError:
            logger.error(f"지원되지 않는 인코딩입니다: {charset}")
            return None
        except UnicodeEncodeError:
            logger.error(
                f"입력 문자열에 선택한 {charset}으로 표현할 수 없는 문자가 포함되어 있습니다."
            )
            return None
        except Exception as e:
            logger.error(f"알 수 없는 인코딩 오류 발생: {str(e)}")
            return None

    @classmethod
    def decode(cls, encoded_text: str, charset: str | None = "utf-8"):
        if not encoded_text or not encoded_text.strip():
            raise ValueError(cls.__is_null_or_empty.format("encoded_text"))

        try:
            decoded_bytes = base64.b64decode(encoded_text, validate=True)
        except Exception as e:
            logger.error(f"Base64 형식이 아니거나 데이터가 손상되었습니다: {e}")
            return None

        try:
            return decoded_bytes.decode(charset)
        except UnicodeDecodeError:
            logger.error(f"지정한 문자셋({charset})으로 해석할 수 없는 데이터입니다.")
            return None
        except LookupError:
            logger.error(f"지원되지 않는 인코딩입니다: {charset}")
            return None
