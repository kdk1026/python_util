from email.message import EmailMessage
import logging
from pathlib import Path
import smtplib

from utils.ini.ini_util import IniUtil

logger = logging.getLogger(__name__)


class MailSenderUtil:
    __is_null_or_empty = "{} is null or empty"

    @classmethod
    def send_email(
        cls,
        config_file_path: str,
        section: str,
        subject: str,
        body: str,
        to_email: str,
        attachment_path: str | None = None,
    ) -> bool:
        """메일 발송
        - config 내용
            - username
            - password
            - host
            - port

        Args:
            config_file_path (str): _description_
            section (str): _description_
            subject (str): _description_
            body (str): _description_
            to_email (str): _description_
            attachment_path (str | None, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        config_dict = IniUtil.get_ini_section(config_file_path, section)

        if config_dict is None:
            return False

        if not subject or not subject.strip():
            raise ValueError(cls.__is_null_or_empty.format("subject"))

        if not body or not body.strip():
            raise ValueError(cls.__is_null_or_empty.format("body"))

        if not to_email or not to_email.strip():
            raise ValueError(cls.__is_null_or_empty.format("body"))

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = config_dict.get("username")
        msg["To"] = to_email
        msg.set_content(body)

        if attachment_path:
            file_path = Path(attachment_path)

            if file_path.exists():
                with open(attachment_path, "rb") as f:
                    file_data = f.read()
                    file_name = file_path.name

                msg.add_attachment(
                    file_data,
                    maintype="application",
                    subtype="octet-stream",
                    filename=file_name,
                )

        try:
            with smtplib.SMTP_SSL(
                config_dict.get("host"), config_dict.get("port")
            ) as smtp:
                smtp.login(config_dict.get("username"), config_dict.get("password"))
                smtp.send_message(msg)
                return True
        except Exception as e:
            logger.error(f"메일 발송 실패: {e}")
            return False
