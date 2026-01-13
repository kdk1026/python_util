import configparser
import logging

logger = logging.getLogger(__name__)


class IniUtil:
    is_null_or_empty = "{} is null or empty"
    is_not_read_file = "파일을 찾을 수 없거나 읽지 못했습니다."

    @classmethod
    def get_ini(cls, file_path: str, section: str, key: str) -> str | None:
        """ini 파일 읽기

        Args:
            file_path (str): _description_
            section (str): _description_
            key (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """

        if not file_path or not file_path.strip():
            raise ValueError(cls.is_null_or_empty.format("file_path"))

        if not section or not section.strip():
            raise ValueError(cls.is_null_or_empty.format("section"))

        if not key or not key.strip():
            raise ValueError(cls.is_null_or_empty.format("key"))

        config = configparser.ConfigParser()

        read_files = config.read(file_path, encoding="utf-8")

        if not read_files:
            logger.error(cls.is_not_read_file)
            return None

        return config[section][key]

    @classmethod
    def get_ini_section(cls, file_path: str, section: str) -> dict | None:
        """ini 파일 읽기

        Args:
            file_path (str): _description_
            section (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            list: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls.is_null_or_empty.format("file_path"))

        if not section or not section.strip():
            raise ValueError(cls.is_null_or_empty.format("section"))

        config = configparser.ConfigParser()

        read_files = config.read(file_path, encoding="utf-8")

        if not read_files:
            logger.error(cls.is_not_read_file)
            return None

        return dict(config.items(section))

    @classmethod
    def get_ini_key(cls, file_path: str, key: str) -> str:
        """ini 파일 읽기

        Args:
            file_path (str): _description_
            key (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls.is_null_or_empty.format("file_path"))

        if not key or not key.strip():
            raise ValueError(cls.is_null_or_empty.format("key"))

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                config_string = "[dummy]\n" + f.read()

            config = configparser.ConfigParser()

            config.read_string(config_string)

            return config.get("dummy", key)
        except FileNotFoundError:
            logger.error(f"Error: File not found at {file_path}")

    @classmethod
    def add_ini(cls, file_path: str, section: str, key: str, value: str) -> None:
        """ini 파일에 추가

        Args:
            file_path (str): _description_
            section (str): _description_
            key (str): _description_
            value (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls.is_null_or_empty.format("file_path"))

        if not section or not section.strip():
            raise ValueError(cls.is_null_or_empty.format("section"))

        if not key or not key.strip():
            raise ValueError(cls.is_null_or_empty.format("key"))

        if not value or not value.strip():
            raise ValueError(cls.is_null_or_empty.format("value"))

        config = configparser.ConfigParser()

        read_files = config.read(file_path, encoding="utf-8")

        if not read_files:
            logger.error(cls.is_not_read_file)
            return None

        if not config.has_section(section):
            config.add_section(section)

        config.set(section, key, value)

        with open(file_path, "w", encoding="utf-8") as f:
            config.write(f)

    @classmethod
    def set_ini(cls, file_path: str, section: str, key: str, value: str) -> None:
        """ini 파일에서 기존 섹션, 키의 값 변경

        Args:
            file_path (str): _description_
            section (str): _description_
            key (str): _description_
            value (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls.is_null_or_empty.format("file_path"))

        if not section or not section.strip():
            raise ValueError(cls.is_null_or_empty.format("section"))

        if not key or not key.strip():
            raise ValueError(cls.is_null_or_empty.format("key"))

        if not value or not value.strip():
            raise ValueError(cls.is_null_or_empty.format("value"))

        config = configparser.ConfigParser()

        read_files = config.read(file_path, encoding="utf-8")

        if not read_files:
            logger.error(cls.is_not_read_file)
            return None

        config.set(section, key, value)

        with open(file_path, "w", encoding="utf-8") as f:
            config.write(f)

    @classmethod
    def clear_ini(cls, file_path: str, section: str) -> None:
        """ini 파일에서 섹션 전체 삭제

        Args:
            file_path (str): _description_
            section (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls.is_null_or_empty.format("file_path"))

        if not section or not section.strip():
            raise ValueError(cls.is_null_or_empty.format("section"))

        config = configparser.ConfigParser()

        read_files = config.read(file_path, encoding="utf-8")

        if not read_files:
            logger.error(cls.is_not_read_file)
            return None

        if config.options(section):
            config.remove_section(section)

            with open(file_path, "w", encoding="utf-8") as f:
                config.write(f)

    @classmethod
    def clear_ini_key(cls, file_path: str, section: str, key: str) -> None:
        """ini 파일에서 특정 키 삭제

        Args:
            file_path (str): _description_
            section (str): _description_
            key (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls.is_null_or_empty.format("file_path"))

        if not section or not section.strip():
            raise ValueError(cls.is_null_or_empty.format("section"))

        if not key or not key.strip():
            raise ValueError(cls.is_null_or_empty.format("key"))

        config = configparser.ConfigParser()

        read_files = config.read(file_path, encoding="utf-8")

        if not read_files:
            logger.error(cls.is_not_read_file)
            return None

        if config[section][key]:
            config.remove_option(section, key)

            with open(file_path, "w", encoding="utf-8") as f:
                config.write(f)
