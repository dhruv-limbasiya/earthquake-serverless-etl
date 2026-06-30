import io

import pandas as pd


def parse_excel(file_bytes):
    """
    Parse Excel file.

    Returns list of dictionaries.
    """

    dataframe = pd.read_excel(
        io.BytesIO(file_bytes)
    )

    return dataframe.to_dict("records")