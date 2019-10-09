import pymysql.cursors
import json

with open('db/settings.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)


class MySQLDB:
    USER = settings.get('USER')
    PASSWORD = settings.get('PASSWORD')
    HOST = settings.get('HOST')

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Подключение к базе данных."""
        self.connection = pymysql.connect(host=self.HOST,
                                          user=self.USER,
                                          password=self.PASSWORD)
        self.cursor = self.connection.cursor()

    def create_db(self):
        """Создание базы данных."""
        try:
            self.cursor.execute('CREATE DATABASE `db_wish_list`')
        except pymysql.err.ProgrammingError:
            pass
        self.cursor.execute('USE `db_wish_list`')

    def create_table(self):
        """Создание таблицы."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `table_wish_list`( `id` INT AUTO_INCREMENT PRIMARY KEY,
                                                                            `name` VARCHAR(48) NOT NULL,
                                                                            `price` VARCHAR(24) NOT NULL,
                                                                            `link` VARCHAR(256) NOT NULL) """)

    def add_item(self, name, price, link):
        """Добавление элемента в таблицу"""
        self.cursor.execute("INSERT INTO table_wish_list VALUES (NULL, '{}', '{}', '{}' )".format(name, price, link))
        self.connection.commit()

    def get_items(self):
        """Получить содержимое таблицы."""
        self.cursor.execute('SELECT * FROM `table_wish_list`')
        rows = self.cursor.fetchall()
        return rows

    def delete_item(self, id):
        """Удаление элемента из таблицы по id."""
        self.cursor.execute('DELETE FROM table_wish_list WHERE id={}'.format(id))
        self.connection.commit()

    def drop_db(self):
        """Удачить базу данных"""
        self.cursor.execute('DROP DATABASE `db_wish_list`')
