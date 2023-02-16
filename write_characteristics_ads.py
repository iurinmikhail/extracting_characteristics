from tqdm import tqdm
import create_card_modeles as ccm
import sentenize as s
import mysql_command as mysql
from config import NAME_TABLES_ALL_ADS, LIMIT

name_column = 'characteristics_core'
name_condition = 'id'

db1 = mysql.CommandMySQL()
for name_table in NAME_TABLES_ALL_ADS:
    s.SET_CORE_ALL_JSON = []
    db1.set_database(name_table, LIMIT)
    db1.create_column_in_tables('characteristics_core')
    select_structural_data = f"""SELECT id, title
                                FROM {name_table}""" \
                             + (f" LIMIT {LIMIT}" if LIMIT else "")
    curs = db1.execute_read_query(select_structural_data)
    for cur in tqdm(curs, desc=f"Запись характеристик в {name_table}"):
        row_id = cur[0]
        result = s.create_core_in_db(cur)
        if not result:
            continue
        characteristics_core = ccm.comparison_core(result)
        if not characteristics_core:
            continue
        db1.update_table(characteristics_core, name_column, name_condition, row_id)
        s.SET_CORE_ALL_JSON.append({'Записано в бд': characteristics_core})
    s.write_json(s.SET_CORE_ALL_JSON, name_table)


