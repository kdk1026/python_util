import logging
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class ByteBufferUtils:
    is_null = "{} is null"
    is_null_or_empty = "{} is null or empty"
    is_negative = "{} is negative"

    @staticmethod
    def to_byte_buffer_str(s: str, encoding: str = "utf-8") -> memoryview:
        if not s or not s.strip():
            raise ValueError(ByteBufferUtils.is_null_or_empty.format("s"))

        encoding = (encoding or "utf-8").strip()

        try:
            byte_data = s.encode(encoding)

            # 자바의 ByteBuffer.wrap(b)와 가장 유사한 형태 (메모리 복사 없이 뷰를 생성)
            return memoryview(byte_data)
        except LookupError:
            logger.error(f"지원되지 않는 인코딩입니다: {encoding}")

    @staticmethod
    def to_byte_buffer_str_list(
        str_list: List[str], encoding: str = "utf-8"
    ) -> Optional[bytearray]:
        if not str_list:
            raise ValueError(ByteBufferUtils.is_null_or_empty.format("str_list"))

        encoding = (encoding or "utf-8").strip()

        buffer = bytearray()

        try:
            for s in str_list:
                # 문자열을 인코딩하여 버퍼에 추가 (자바의 buffer.put 역할)
                buffer.extend(s.encode(encoding))
        except LookupError:
            logger.error(f"지원되지 않는 인코딩입니다: {encoding}")
            return None

        return buffer

    @staticmethod
    def to_byte_buffer_object(obj: Any, encoding: str = "utf-8") -> Optional[bytearray]:
        encoding = (encoding or "utf-8").strip()

        if obj is None:
            raise ValueError(ByteBufferUtils.is_null_or_empty.format("obj"))

        buffer = bytearray()

        try:
            attrs = vars(obj)

            for value in attrs.values():
                str_value = str(value) if value is not None else ""

                # 문자열을 인코딩하여 버퍼에 추가 (자바의 buffer.put 역할)
                buffer.extend(str_value.encode(encoding))
        except (LookupError, AttributeError, TypeError) as e:
            logger.error(f"Error processing object to byte_buffer: {e}", exc_info=True)
            return None

        return buffer

    @staticmethod
    def to_byte_buffer_object_list(
        obj_list: List[Any], encoding: str = "utf-8"
    ) -> Optional[bytearray]:
        encoding = (encoding or "utf-8").strip()

        if not obj_list:
            raise ValueError(ByteBufferUtils.is_null_or_empty.format("obj_list"))

        buffer = bytearray()

        try:
            for obj in obj_list:
                if obj is None:
                    continue

                attrs = vars(obj)

                for value in attrs.values():
                    str_value = str(value) if value is not None else ""

                    # 문자열을 인코딩하여 버퍼에 추가 (자바의 buffer.put 역할)
                    buffer.extend(str_value.encode(encoding))
        except (LookupError, AttributeError, TypeError) as e:
            logger.error(
                f"Error processing object list to byte_buffer: {e}", exc_info=True
            )
            return None

        return buffer

    @staticmethod
    def to_byte_buffer_map(
        data_map: Dict[str, Any], encoding: str = "utf-8"
    ) -> Optional[bytearray]:
        encoding = (encoding or "utf-8").strip()

        if not data_map:
            raise ValueError(ByteBufferUtils.is_null_or_empty.format("data_map"))

        buffer = bytearray()

        try:
            for value in data_map.values():
                str_value = str(value) if value is not None else "None"

                # 문자열을 인코딩하여 버퍼에 추가 (자바의 buffer.put 역할)
                buffer.extend(str_value.encode(encoding))
        except LookupError:
            logger.error(f"지원되지 않는 인코딩입니다: {encoding}")
            return None
        except Exception as e:
            logger.error(f"Error processing map to byte_buffer: {e}", exc_info=True)
            return None

        return buffer

    @staticmethod
    def to_byte_buffer_map_list(
        dict_list: List[Dict[str, Any]], encoding: str = "utf-8"
    ) -> Optional[bytearray]:
        encoding = (encoding or "utf-8").strip()

        if not dict_list:
            raise ValueError(ByteBufferUtils.is_null_or_empty.format("dict_list"))

        buffer = bytearray()

        try:
            for data_map in dict_list:
                # dict 타입의 인스턴스인지 확인
                if not isinstance(data_map, dict):
                    continue

                for value in data_map.values():
                    str_value = str(value) if value is not None else ""

                    # 문자열을 인코딩하여 버퍼에 추가 (자바의 buffer.put 역할)
                    buffer.extend(str_value.encode(encoding))
        except LookupError:
            logger.error(f"지원되지 않는 인코딩입니다: {encoding}")
            return None
        except Exception as e:
            logger.error(f"Error processing map to byte_buffer: {e}", exc_info=True)
            return None

        return buffer

    @staticmethod
    def get_byte_buffer_from_byte_array(
        bytes_array: Union[bytes, bytearray],
    ) -> memoryview:
        if bytes_array is None:
            raise ValueError(ByteBufferUtils.is_null.format("bytes_array"))

        # 자바의 ByteBuffer.wrap(b)와 가장 유사한 형태 (메모리 복사 없이 뷰를 생성)
        return memoryview(bytes_array)

    @staticmethod
    def get_byte_array_from_byte_buffer(
        byte_buffer: Union[memoryview, bytearray, bytes],
    ) -> bytes:
        if byte_buffer is None:
            raise ValueError(ByteBufferUtils.is_null.format("byte_buffer"))

        """
        memoryview나 bytearray 객체는 .tobytes()를 호출하면
        현재 버퍼에 담긴 내용을 새로운 bytes 객체로 복사하여 반환
        (자바의 buffer.get 역할)
        """
        if hasattr(byte_buffer, "tobytes"):
            return byte_buffer.tobytes()

        # 이미 bytes 객체라면 그대로 반환
        return bytes(byte_buffer)

    @staticmethod
    def get_byte_array_from_byte_buffer_limit(
        byte_buffer: Union[memoryview, bytearray, bytes], new_position: int, limit: int
    ) -> bytes:
        if byte_buffer is None:
            raise ValueError(ByteBufferUtils.is_null.format("byte_buffer"))

        # 파이썬은 정수가 객체이므로 None 체크가 가능
        if new_position is None or limit is None:
            raise ValueError(ByteBufferUtils.is_null.format("position or limit"))

        try:
            return (
                byte_buffer[new_position:limit].tobytes()
                if hasattr(byte_buffer, "tobytes")
                else bytes(byte_buffer[new_position:limit])
            )
        except IndexError as e:
            raise IndexError(f"Position or limit out of bounds: {e}")

    @staticmethod
    def get_byte_array_from_byte_buffer_length(
        byte_buffer: Union[memoryview, bytearray, bytes], new_position: int, length: int
    ) -> bytes:
        if byte_buffer is None:
            raise ValueError(ByteBufferUtils.is_null.format("byte_buffer"))

        # 파이썬은 정수가 객체이므로 None 체크가 가능
        if new_position is None or length is None:
            raise ValueError(ByteBufferUtils.is_null.format("position or length"))

        limit = new_position + length

        try:
            if limit > len(byte_buffer):
                raise IndexError("Requested length exceeds buffer size")

            return (
                byte_buffer[new_position:limit].tobytes()
                if hasattr(byte_buffer, "tobytes")
                else bytes(byte_buffer[new_position:limit])
            )
        except IndexError as e:
            raise IndexError(f"Position or length out of bounds: {e}")
