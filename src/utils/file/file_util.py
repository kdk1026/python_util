import logging
from pathlib import Path
from datetime import datetime
import shutil

logger = logging.getLogger(__name__)


class FileUtil:
    """
    Author: 김대광
    """

    _is_null_or_empty = "{} is null or empty"
    _is_negative = "{} is negative"

    @classmethod
    def is_exists_file(cls, file_path: str) -> bool:
        """파일의 존재여부 확인

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        path = Path(file_path)
        return path.exists()

    @classmethod
    def get_filename(cls, file_path: str) -> str:
        """해당 경로에서 파일명 추출

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
        return path.name

    @classmethod
    def get_file_extension(cls, file_name: str) -> str:
        """파일 확장자 구하기

        Args:
            file_name (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not file_name or not file_name.strip():
            raise ValueError(cls._is_null_or_empty.format("file_name"))

        path = Path(file_name)
        return path.suffix.replace(".", "")

    @classmethod
    def get_file_size(cls, file_path: str) -> int:
        """파일 용량 구하기

        Args:
            file_path (str): _description_

        Returns:
            int: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        path = Path(file_path)
        return path.stat().st_size

    @classmethod
    def readable_file_size(cls, file_size: int) -> str:
        """파일 용량, 읽기 편한 단위로 변환
        - - B, KB, MB, GB, TB

        Args:
            file_size (int): _description_

        Returns:
            str: _description_
        """
        if file_size < 0:
            raise ValueError(cls._is_null_or_empty.format("file_size"))

        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if file_size < 1024:
                return f"{file_size:.2f} {unit}"
            file_size /= 1024

    @classmethod
    def last_modified(cls, file_path: str) -> str:
        """파일의 수정한 날짜 구하기

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
        mtime = path.stat().st_mtime

        last_modified_date = datetime.fromtimestamp(mtime)
        return last_modified_date.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def write_file(cls, file_path: str, text: str) -> None:
        """텍스트 내용을 해당 경로에 파일로 생성

        Args:
            file_path (str): _description_
            text (str): _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        if not text or not text.strip():
            raise ValueError(cls._is_null_or_empty.format("text"))

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

    @classmethod
    def write_file_encodig(cls, file_path: str, text: str, encoding: str) -> None:
        """텍스트 내용을 해당 경로에 파일로 생성

        Args:
            file_path (str): _description_
            text (str): _description_
            encoding (str): _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        if not text or not text.strip():
            raise ValueError(cls._is_null_or_empty.format("text"))

        if not encoding or not encoding.strip():
            raise ValueError(cls._is_null_or_empty.format("encoding"))

        with open(file_path, "w", encoding=encoding) as f:
            f.write(text)

    @classmethod
    def read_file(cls, file_path: str) -> str:
        """파일을 텍스트로 읽음

        Args:
            file_path (str): _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return content

    @classmethod
    def read_file_encodig(cls, file_path: str, encoding: str) -> str:
        """파일을 텍스트로 읽음

        Args:
            file_path (str): _description_
            encoding (str): _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()

        return content

    @classmethod
    def delete_file(cls, file_path: str) -> None:
        """파일 삭제

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        path = Path(file_path)

        # missing_ok=True를 설정하면 파일이 없어도 에러를 내지 않고 넘어감 (파이썬 3.8+)
        # path.unlink(missing_ok=True)

        path.unlink()

    @classmethod
    def copy_file(cls, src_file_path: str, dest_file_path: str) -> None:
        """파일 복사

        Args:
            src_file_path (str): _description_
            dest_file_path (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
        """
        if not src_file_path or not src_file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("src_file_path"))

        if not dest_file_path or not dest_file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("dest_file_path"))

        shutil.copy(src_file_path, dest_file_path)

    @classmethod
    def get_all_file_list(cls, file_path: str) -> list:
        """해당 경로의 모든 파일 및 디렉토리를 반환

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            list: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        path = Path(file_path)

        if not path.exists():
            return []

        return [f.name for f in path.iterdir()]

    @classmethod
    def get_file_list(cls, file_path: str) -> list:
        """해당 경로의 파일 반환

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            list: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        path = Path(file_path)

        if not path.exists():
            return []

        return [f.name for f in path.iterdir() if f.is_file()]

    @classmethod
    def get_directory_list(cls, file_path: str) -> list:
        """해당 경로의 디렉토리 반환

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            list: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        path = Path(file_path)

        if not path.exists():
            return []

        return [f.name for f in path.iterdir() if f.is_dir()]

    @classmethod
    def convert_file_to_bytes(cls, file_path: str) -> bytes | None:
        """파일을 byte[]로 변환

        Args:
            file_path (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            bytes | None: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        path = Path(file_path)

        try:
            return path.read_bytes()
        except FileNotFoundError:
            logger.error(f"Error: File not found at {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None
