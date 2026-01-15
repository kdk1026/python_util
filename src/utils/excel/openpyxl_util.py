import copy
import logging
import os
from pathlib import Path
import re
import openpyxl
from openpyxl.styles import Font, PatternFill

logger = logging.getLogger(__name__)


class OpenpyxlUtil:
    """
    Author: 김대광
    """

    _is_null_or_empty = "{} is null or empty"

    @classmethod
    def read_excel(
        cls, file_path: str, cell_names: list = None, is_decimal: bool = False
    ) -> list:
        """엑셀 파일 읽기

        Args:
            file_path (str): _description_
            cell_names (list, optional): _description_. Defaults to None.
            is_decimal (bool, optional): _description_. Defaults to False.

        Raises:
            ValueError: _description_
            FileNotFoundError: _description_

        Returns:
            _type_: _description_
        """
        if not file_path or not file_path.strip():
            raise ValueError(cls._is_null_or_empty.format("file_path"))

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        cell_names = cell_names or []
        res_list = []

        try:
            wb = openpyxl.load_workbook(file_path, data_only=True)
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2):
                row_map = {
                    name: cls.__get_cell_value(cell, is_decimal)
                    for name, cell in zip(cell_names, row)
                }

                res_list.append(row_map)

            return res_list
        except Exception as e:
            logger.error(f"Error: {e}")
            return []

    @classmethod
    def _get_cell_value(cls, cell, is_decimal: bool):
        val = cell.value

        if val is None:
            return ""

        if isinstance(val, (int, float)):
            return val if is_decimal else int(val)

        return val

    @staticmethod
    def write_excel(
        dest_path: str, file_name: str, contents_list: list, cell_titles: list
    ):
        """엑셀 파일 생성

        Args:
            dest_path (str): _description_
            file_name (str): _description_
            contents_list (list): _description_
            cell_titles (list): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if not all([dest_path, file_name, contents_list, cell_titles]):
            raise ValueError("모든 인자값은 필수이며 비어있을 수 없습니다.")

        wb = openpyxl.Workbook()
        ws = wb.active

        ws.append(cell_titles)

        header_font = Font(bold=True)
        header_fill = PatternFill(
            start_color="D3D3D3", end_color="D3D3D3", fill_type="solid"
        )

        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill

        for content in contents_list:
            row_data = [content.get(title, "") for title in cell_titles]
            ws.append(row_data)

        full_path = os.path.join(dest_path, file_name)

        try:
            wb.save(full_path)
            return True
        except Exception as e:
            logger.error(f"Error saving excel: {e}")
            return False

    @classmethod
    def write_excel_template(
        cls,
        template_file_path: str,
        dest_file_path: str,
        file_name: str,
        contents_list: list,
        template_row_range: tuple = (2, 1),
    ):
        """템플릿 파일 이용해서 엑셀 파일 생성

        Args:
            template_file_path (str): _description_
            dest_file_path (str): _description_
            file_name (str): _description_
            contents_list (list): _description_
            template_row_range (tuple, optional): _description_. Defaults to (1, 1).

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            _type_: _description_

        템플릿 작성:
            {{id}} | {{name}}
        """
        if not template_file_path or not template_file_path.strip():
            raise ValueError(cls._is_null_or_empty("template_file_path"))

        if not dest_file_path or not dest_file_path.strip():
            raise ValueError(cls._is_null_or_empty("dest_file_path"))

        if not file_name or not file_name.strip():
            raise ValueError(cls._is_null_or_empty("file_name"))

        if not contents_list:
            raise ValueError(cls._is_null_or_empty("contents_list"))

        try:
            wb = openpyxl.load_workbook(template_file_path)
            ws = wb.active

            # 템플릿 정보 추출 및 캐싱
            start_row, end_row = template_row_range
            template_rows_cache = cls._extract_template_cache(ws, start_row, end_row)

            # 데이터 쓰기 실행
            cls._render_contents_to_sheet(
                ws, contents_list, template_rows_cache, start_row
            )

            os.makedirs(dest_file_path, exist_ok=True)
            save_path = os.path.join(dest_file_path, file_name)
            wb.save(save_path)
            return True
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return False

    @staticmethod
    def _extract_template_cache(ws, start_row: int, end_row: int) -> list:
        """템플릿 영역의 서식과 값을 캐시로 추출"""
        cache = []
        for r in range(start_row, end_row + 1):
            row_cells = []
            for c in range(1, ws.max_column + 1):
                cell = ws.cell(row=r, column=c)
                row_cells.append(
                    {
                        "value": cell.value,
                        "font": copy.copy(cell.font),
                        "border": copy.copy(cell.border),
                        "fill": copy.copy(cell.fill),
                        "number_format": cell.number_format,
                        "alignment": copy.copy(cell.alignment),
                        "protection": copy.copy(cell.protection),
                    }
                )
            cache.append(row_cells)
        return cache

    @classmethod
    def _render_contents_to_sheet(
        cls, ws, contents_list, template_rows_cache, start_row
    ):
        """캐시된 템플릿을 바탕으로 데이터를 시트에 기록"""
        template_height = len(template_rows_cache)

        for index, data in enumerate(contents_list):
            current_start_row = start_row + (index * template_height)

            for r_idx, row_content in enumerate(template_rows_cache):
                target_row = current_start_row + r_idx

                for c_idx, cell_info in enumerate(row_content, 1):
                    target_cell = ws.cell(row=target_row, column=c_idx)

                    # 서식 복사
                    cls._apply_cell_style(target_cell, cell_info)

                    # 플레이스홀더 치환 및 값 입력
                    val = cell_info["value"]
                    if isinstance(val, str) and "{{" in val:
                        val = cls._replace_placeholders(val, data)

                    target_cell.value = val

    @staticmethod
    def _apply_cell_style(target_cell, cell_info):
        """셀에 서식 적용"""
        target_cell.font = cell_info["font"]
        target_cell.border = cell_info["border"]
        target_cell.fill = cell_info["fill"]
        target_cell.number_format = cell_info["number_format"]
        target_cell.alignment = cell_info["alignment"]

    @staticmethod
    def _replace_placeholders(text: str, data: dict) -> str:
        """{{key}} 형태의 문구를 데이터로 치환"""
        matches = re.findall(r"\{\{(.*?)\}\}", text)
        for match in matches:
            key = match.strip()
            if key in data:
                text = text.replace(f"{{{{{match}}}}}", str(data[key]))
        return text
