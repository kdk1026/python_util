from io import BytesIO
import io
import logging
import mimetypes
from pathlib import Path
from PIL import UnidentifiedImageError
import magic
from PIL import Image


logger = logging.getLogger(__name__)


class FileTypeUtil:
    """
    Author: 김대광
    """

    _is_null = "{} is null"
    _is_null_or_empty = "{} is null or empty"
    _is_negative = "{} is negative"

    @classmethod
    def get_file_mime_type(cls, file_path: str) -> str | None:
        """파일 MIME Type 구하기
        - 정확성 떨어짐
        - 확장자 기반

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        path = Path(file_path)
        if not path.exists():
            logger.error(f"Error: File not found at {file_path}")
            return None

        mime_type, _ = mimetypes.guess_type(file_path)

        if mime_type is None:
            return "application/octet-stream"

        return mime_type

    @classmethod
    def get_file_mime_type_magic(cls, file_path: str) -> str | None:
        """파일 MIME Type 구하기
        - python-magic 사용
        - 정확성 높음
        - 실제 데이터(바이트)를 읽어서 분석

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str | None: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        try:
            magic.Magic(mime_encoding=True)
            return magic.from_file(file_path, mime=True)
        except FileNotFoundError:
            logger.error(f"Error: File not found at {file_path}")
            return None

    @classmethod
    def is_all_file(cls, extension: str, mime_type: str) -> bool:
        """파일 체크

        Args:
            extension (str): _description_
            mime_type (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not extension or not extension.strip():
            raise ValueError(cls._is_null_or_empty.format("extension"))

        if not mime_type or not mime_type.strip():
            raise ValueError(cls._is_null_or_empty.format("mime_type"))

        ext_arr = (
            "jpg",
            "jpeg",
            "png",
            "gif",
            "pdf",
            "doc",
            "docx",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
            "hwp",
            "txt",
            "zip",
            "rar",
            "7z",
        )

        mime_arr = (
            "image/jpeg",
            "image/png",
            "image/gif",
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/x-hwp",
            "application/haansofthwp",
            "application/vnd.hancom.hwp",
            "text/plain",
            "application/zip",
            "application/x-rar-compressed",
            "application/x-7z-compressed",
        )

        return (extension in ext_arr) and (mime_type in mime_arr)

    @classmethod
    def is_img_file(cls, extension: str, mime_type: str) -> bool:
        """이미지 파일 체크

        Args:
            extension (str): _description_
            mime_type (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not extension or not extension.strip():
            raise ValueError(cls._is_null_or_empty.format("extension"))

        if not mime_type or not mime_type.strip():
            raise ValueError(cls._is_null_or_empty.format("mime_type"))

        ext_arr = ("jpg", "jpeg", "png", "gif")

        mime_arr = ("image/jpeg", "image/png", "image/gif")

        return (extension in ext_arr) and (mime_type in mime_arr)

    @classmethod
    def is_valid_image(cls, image_stream: bytes | BytesIO) -> bool:
        """이미지 파일이 올바른 이미지 형식이거나 손상되지 않았는지 체크

        Args:
            image_stream (bytes | BytesIO): _description_

        Raises:
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not image_stream:
            raise ValueError(cls._is_null.format("image_stream"))

        if isinstance(image_stream, bytes):
            image_stream = io.BytesIO(image_stream)

        try:
            with Image.open(image_stream) as img:
                img.verify()

            return True
        except (UnidentifiedImageError, IOError):
            return False

    @classmethod
    def is_doc_file(cls, extension: str, mime_type: str) -> bool:
        """문서 파일 체크

        Args:
            extension (str): _description_
            mime_type (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not extension or not extension.strip():
            raise ValueError(cls._is_null_or_empty.format("extension"))

        if not mime_type or not mime_type.strip():
            raise ValueError(cls._is_null_or_empty.format("mime_type"))

        ext_arr = ("pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "hwp", "txt")

        mime_arr = (
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/x-hwp",
            "application/haansofthwp",
            "application/vnd.hancom.hwp",
            "text/plain",
        )

        return (extension in ext_arr) and (mime_type in mime_arr)

    @classmethod
    def is_archive_file(cls, extension: str, mime_type: str) -> bool:
        """압축 파일 체크

        Args:
            extension (str): _description_
            mime_type (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not extension or not extension.strip():
            raise ValueError(cls._is_null_or_empty.format("extension"))

        if not mime_type or not mime_type.strip():
            raise ValueError(cls._is_null_or_empty.format("mime_type"))

        ext_arr = ("zip", "rar", "7z")

        mime_arr = (
            "application/zip",
            "application/x-rar-compressed",
            "application/x-7z-compressed",
        )

        return (extension in ext_arr) and (mime_type in mime_arr)

    @classmethod
    def is_audio_file(cls, extension: str, mime_type: str) -> bool:
        """오디오 파일 체크

        Args:
            extension (str): _description_
            mime_type (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not extension or not extension.strip():
            raise ValueError(cls._is_null_or_empty.format("extension"))

        if not mime_type or not mime_type.strip():
            raise ValueError(cls._is_null_or_empty.format("mime_type"))

        ext_arr = ("mp3", "wav")

        mime_arr = ("audio/mpeg", "audio/wav")

        return (extension in ext_arr) and (mime_type in mime_arr)

    @classmethod
    def is_video_file(cls, extension: str, mime_type: str) -> bool:
        """비디오 파일 체크

        Args:
            extension (str): _description_
            mime_type (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not extension or not extension.strip():
            raise ValueError(cls._is_null_or_empty.format("extension"))

        if not mime_type or not mime_type.strip():
            raise ValueError(cls._is_null_or_empty.format("mime_type"))

        ext_arr = ("mp4", "avi", "mov", "mkv")

        mime_arr = (
            "video/mp4",
            "video/x-msvideo",
            "video/quicktime",
            "video/x-matroska",
        )

        return (extension in ext_arr) and (mime_type in mime_arr)

    @classmethod
    def is_runable_file(cls, extension: str) -> bool:
        """실행 파일 체크
        - 결과가 true면 업로드 불가, false면 업로드 가능

        Args:
            extension (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not extension or not extension.strip():
            raise ValueError(cls._is_null_or_empty.format("extension"))

        ext_arr = (
            "bat",
            "bin",
            "cmd",
            "com",
            "cpl",
            "dll",
            "exe",
            "gadget",
            "inf1",
            "ins",
            "isu",
            "jse",
            "lnk",
            "msc",
            "msi",
            "msp",
            "mst",
            "paf",
            "pif",
            "ps1",
            "reg",
            "rgs",
            "scr",
            "sct",
            "sh",
            "shb",
            "shs",
            "u3p",
            "vb",
            "vbe",
            "vbs",
            "vbscript",
            "ws",
            "wsf",
            "wsh",
        )

        return extension in ext_arr
