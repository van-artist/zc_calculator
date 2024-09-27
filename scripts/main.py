import os
import data_processor
from typing import List
from data_processor import read_tables_from_folder,save_major_to_json,table_process,major_process

BASE_PATH: str = os.path.dirname(os.path.abspath(__file__))
DATA_PATH: str = os.path.join(BASE_PATH, '../data')
OUTPUT_PATH: str= os.path.join(BASE_PATH, '../out')
# 调用函数读取表格项
tables = read_tables_from_folder(DATA_PATH)
majors:List[data_processor.Major]=[]
# 处理第一个表格示例
if tables:
    for table in tables:
        major=table_process(table=table["table_data"])
        save_major_to_json(major,filename=os.path.join(OUTPUT_PATH,major.name+".json"))
        majors.append(major)
else:
    print("No tables found in the provided directory.")
major_process(majors[0])
