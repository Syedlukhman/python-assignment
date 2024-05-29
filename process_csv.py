import pandas as pd
from sqlalchemy import create_engine
from db import DataBase

class ProcessCsv(DataBase):
    def __init__(self, db_instance, dataset_path, file_names, file_to_table_map):
        super().__init__(db_instance.host, db_instance.database_name, db_instance.username, db_instance.password, db_instance.port, db_instance.tables)
        self.dataset_path = dataset_path
        self.file_names = file_names
        self.file_to_table_map = file_to_table_map
        connection_string = f"mysql+mysqlconnector://{db_instance.username}:{db_instance.password}@{db_instance.host}:{db_instance.port}/{db_instance.database_name}"
        self.engine = create_engine(connection_string)

    def insert_csv_data(self):
        if self.engine is None:
            print("Engine has not been initialized!!")
            return
        
        column_names = {file_name: [col[0] for col in self.tables[self.file_to_table_map[file_name]]] for file_name in self.file_names}

        dataframes = {}

        for file_name in self.file_names:
            csv_path = f'{self.dataset_path}/{file_name}'
            
            with open(csv_path, 'r') as csvfile:
                first_line = csvfile.readline()
                num_columns_in_csv = len(first_line.split(','))
            
            cols_to_use = column_names[file_name][:num_columns_in_csv] if num_columns_in_csv <= len(column_names[file_name]) else column_names[file_name]
            
            df = pd.read_csv(csv_path, names=cols_to_use, header=0)
            table_name = self.file_to_table_map[file_name]
            df.to_sql(name=table_name, con=self.engine, if_exists='replace', index=False)
            print(f'Data Copied to {table_name} in SQL')
            
            name_key = file_name.replace('.csv', '')
            dataframes[name_key] = df

    def get_csv_data(self, table_name):
        if not self.engine:
            print("Error: Database connection not established.")
            return None
        try:
            return pd.read_sql_table(table_name, con=self.engine)
        except Exception as e:
            print(f"Error reading data from {table_name}: {e}")
            return f"Error reading data from {table_name}: {e}"
