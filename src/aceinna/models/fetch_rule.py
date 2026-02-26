from dataclasses import dataclass
from typing import Literal

@dataclass
class DataSourceFetchRule:
    name: str = ""
    file_type: Literal['xlsx', 'csv'] = 'csv'
    message_id_col_index: int = 1
    message_data_col_index: int = 2
    timestamp_col_index: int = 0
    ignore_first_row: bool = True
