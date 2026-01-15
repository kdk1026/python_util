import logging
import socket
import ssl

logger = logging.getLogger(__name__)


class PortChecker:
    """
    Author: 김대광
    """

    __is_null_or_empty = "{} is null or empty"

    @classmethod
    def is_connected(cls, host: str, port: int) -> bool:
        if not host or not host.strip():
            raise ValueError(cls.__is_null_or_empty.format("host"))

        if not (0 <= port <= 65535):
            raise ValueError("port must be between 0 and 65535")

        # 1. 최신 프로토콜(TLS)을 사용하도록 컨텍스트 생성
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

        # 2. 취약한 이전 버전(TLS 1.0, 1.1) 사용 금지
        context.minimum_version = ssl.TLSVersion.TLSv1_2

        # 3. 시스템의 기본 신뢰 로드 (CA 인증서 확인)
        context.load_default_certs()

        try:
            with socket.create_connection((host, port), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=host):
                    return True
        except (socket.timeout, socket.error, ssl.SSLError) as e:
            logger.error(f"Connection failed: {e}")
            return False
