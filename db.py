import mysql.connector

class DataBase:
    def __init__(self, host, database_name, username, password, port, tables):
        self.host = host
        self.database_name = database_name
        self.username = username
        self.password = password
        self.port = port
        self.tables = tables
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            port=self.port
        )

    def create_database(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
            print(f"Database '{self.database_name}' created successfully!!")
        except mysql.connector.Error as err:
            print(f"Error creating database: {err}")
        finally:
            cursor.close()

    def create_tables(self):
        self.connection.database = self.database_name
        cursor = self.connection.cursor()
        for table_name, columns in self.tables.items():
            try:
                create_table_command = f"CREATE TABLE {table_name} ("
                col_definitions = [f"[{col_name}] {data_type}" for col_name, data_type in columns]
                create_table_command += ", ".join(col_definitions)
                create_table_command += ")"
                print(f"Table '{table_name}' created successfully.")
            except mysql.connector.Error as err:
                print(f"Failed creating table '{table_name}': {err}")
        cursor.close()

    def close_connection(self):
        if self.connection:
            self.connection.close()

