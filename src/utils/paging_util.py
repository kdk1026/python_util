import math
import re


class PagingUtil:
    """
    Author: 김대광
    """

    __is_null_or_empty = "{} is null or empty"
    __is_negative = "{} is negative"

    def __init__(
        self,
        page_per_row: int,
        page_per_screen: int,
        total_cnt: int,
        current_page_str: str,
        link_url: str | None = None,
    ):
        if page_per_row <= 0:
            raise ValueError(self.__is_negative.format("page_per_row"))

        if page_per_screen <= 0:
            raise ValueError(self.__is_negative.format("page_per_screen"))

        if total_cnt <= 0:
            raise ValueError(self.__is_negative.format("total_cnt"))

        if not current_page_str or not current_page_str.strip():
            raise ValueError(self.__is_null_or_empty.format("current_page_str"))

        if not bool(re.match("^\\d+$", current_page_str)):
            raise ValueError("current_page_str not number")

        # 페이지당 행수, MySQL LIMIT
        self.page_per_row = page_per_row

        # 화면당 페이지수
        self.page_per_screen = page_per_screen

        # 전체 행수(데이터 건수)
        self.total_cnt = total_cnt

        self.current_page = int(current_page_str)

        # 링크 URL
        self.link_url = link_url

        # 전체 페이지수
        self.total_page = (self.total_cnt + self.page_per_row - 1) // self.page_per_row

        # 현재 페이지 번호
        self.current_page = max(1, min(self.current_page, self.total_page))

        current_block = (self.current_page - 1) // self.page_per_screen

        # 시작 페이지 번호
        self.first_page = (current_block * self.page_per_screen) + 1

        # 종료 페이지 번호
        self.last_page = min(
            self.first_page + self.page_per_screen - 1, self.total_page
        )

        # 이전 블럭 페이지 번호
        self.prev_block_page = max(1, self.first_page - 1)

        # 다음 블럭 페이지 번호
        self.next_block_page = min(self.last_page + 1, self.total_page)

        # MySQL OFFSET
        self.offset = (self.current_page - 1) * self.page_per_row

        # SQL 시작 행번호
        # MySQL의 경우 -1 (0부터 시작) 또는 offSet 사용
        self.start = self.offset + 1

        # SQL 종료 행번호
        # MySQL의 경우 사용안함
        self.end = min(self.current_page * self.page_per_row, self.total_cnt)

        # 전체 블럭
        self.total_block = (
            self.total_page + self.page_per_screen - 1
        ) // self.page_per_screen

    def __str__(self):
        return str(self.__dict__)
