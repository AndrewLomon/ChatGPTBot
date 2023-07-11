import sqlite3



class BotDB:
    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        self.conn = sqlite3.connect((db_file))
        print('Базза данных подключилась!')
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в БД"""
        result = self.cursor.execute("SELECT key FROM clients WHERE user_id=?", (user_id,))
        return bool(len(result.fetchall()))

    def get_client_key(self, user_id):
        """Получаем id юзера в базе по его user_id в телеграмме"""
        result = self.cursor.execute("SELECT key FROM clients WHERE user_id=?", (user_id,))
        return result.fetchone()[0]


    def add_client(self, user_id, join_date, user_name, token_count):
        """Добавляем клиента в БД"""
        self.cursor.execute("INSERT INTO clients ('user_id', 'join_date', 'user_name', 'token_count')"
                            "VALUES (?, ?, ?, ?)",
                            (user_id, join_date, user_name, token_count))
        return self.conn.commit()

    def get_client_info(self):
        query = "SELECT * FROM clients"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def get_client_tokens(self, user_id):
        query = "SELECT token_count FROM clients WHERE user_id=?"
        self.cursor.execute(query, (user_id,))
        data = self.cursor.fetchall()[0]
        return data

    def count_client_tokens(self, token_count, user_id):
        query = "UPDATE clients SET token_count = token_count - ? WHERE user_id=?"
        self.cursor.execute(query, (token_count, user_id))
        return self.conn.commit()

    def update_client_tokens(self, token_count):
        query = "UPDATE clients SET token_count=?"
        self.cursor.execute(query, (token_count,))
        return self.conn.commit()

    def admin_exists(self, user_id):
        """Проверяем, есть ли админ в БД"""
        result = self.cursor.execute("SELECT key FROM admins WHERE admin_id=?", (user_id,))
        return bool(len(result.fetchall()))

    def add_admin(self, user_id, user_name, join_date):
        """Добавляем админа в БД"""
        self.cursor.execute("INSERT INTO admins ('admin_id', 'admin_name', 'join_date') VALUES (?, ?, ?)",
                            (user_id, user_name, join_date))
        return self.conn.commit()

    def delete_admin(self, user_id,):
        """Удаляем админа из БД"""
        self.cursor.execute("DELETE FROM admins WHERE admin_id=?",
                            (user_id,))
        return self.conn.commit()

    def get_admin_id(self):
        """Берём айди всех админов"""
        query = "SELECT admin_id FROM admins"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def get_admin_list(self):
        """Берём айди всех админов"""
        query = "SELECT * FROM admins"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()
