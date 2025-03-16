from typing import Any
import re
import pandas as pd


def parse_excel(file_name: str) -> tuple[tuple[Any]]:
    excel_pattern = r".*\.(xls|xlsx|xlsm|xlsb)$"
    if not re.match(excel_pattern, file_name):
        raise TypeError("The file must have an excel-compatible extension.")

    df = pd.read_excel(file_name)

    parsed_data = []

    for _, row in df.iterrows():
        parsed_data.append(tuple(row))

    return tuple(parsed_data)
