from mysql.connector import Error
import mysql.connector
import config as c


class CommandMySQL:
    """Класс для подключения к базе данных и работе с таблицами
    Заполнить параметры для подключения в переменные класса
    """
    SERVER = c.SERVER
    PORT = c.PORT
    LOGIN = c.LOGIN
    PASSWORD = c.PASSWORD
    DATABASE = c.DATABASE

    def __init__(self):
        self.db_table = None
        self.limit = None
        self.offset = None
        self.connection = self._create_connection()

    def get_database(self):
        return self.db_table, self.limit, self.offset

    def set_database(self, db, limit=0, offset=0):
        self.db_table = db
        self.limit = limit
        self.offset = offset

    def _create_connection(self):
        """Подключает к базе данных
        """
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.SERVER,
                port=self.PORT,
                user=self.LOGIN,
                password=self.PASSWORD,
                database=self.DATABASE
            )
            print(f"Подключился к базе данных {self.DATABASE} ")
        except Error as e:
            print(f"Произошла ошибка при подключении к базе данных{self.DATABASE} {e}")
        return connection

    def execute_query(self, query: str, values=None):
        """Изменяет таблицу
        """
        cursor = self.connection.cursor()
        try:
            if values is not None:
                cursor.execute(query, (values,))
            else:
                cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"Произошла ошибка {e}")

    def execute_read_query(self, query: str, as_dict: bool = False):
        """Читает данные из таблицы.
        query: Запрос к базе данных.
        as_dict: если True, то на выходе итератор со словарем,
                если False, то на выходе итератор со строкой.
        """
        if as_dict:
            cursor = self.connection.cursor(dictionary=True)
        else:
            cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return (i for i in result)
        except Error as e:
            print(f"The error '{e}' occurred")

    def update_table(self, new_data: list, name_column: str, name_condition: str, value_condition: str):
        """Записывает данные в столбец
        new_characteristics: характеристики для записи;
        name_column: Наименование столбца, в котором обновляем данные;
        name_condition: Столбец условия;
        value_condition: Строка условия;
        """

        update_characteristics = f"""UPDATE {self.db_table} 
                                    SET {name_column} = \"{new_data}\" 
                                    WHERE {name_condition} = {value_condition};"""
        self.execute_query(update_characteristics)

    def this_column_exists(self, name_new_column: str) -> bool:
        """Проверяет существование столбца
         name_new_column: наименование столбца, существование которого проверяется
         """
        command_check_column = f"""SELECT COLUMN_NAME 
                                FROM INFORMATION_SCHEMA.COLUMNS 
                                WHERE TABLE_NAME = '{self.db_table}';"""
        colum_name = self.execute_read_query(command_check_column)
        return all(map(lambda x: name_new_column not in ''.join(x), colum_name))

    def create_column_in_tables(self, name_new_column: str):
        """Создает столбец, если его нет
        name_new_column: Наименование столбца
        """
        if self.this_column_exists(name_new_column):
            create_column = f"""ALTER TABLE {self.db_table} ADD COLUMN {name_new_column} LONGTEXT"""
            self.execute_query(create_column)










