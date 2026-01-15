import logging
import os
from pathlib import Path
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
