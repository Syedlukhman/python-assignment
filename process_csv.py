import pandas as pd
from sqlalchemy import create_engine
from db import DataBase

class ProcessCsv(DataBase):
    def __init__(self, db_instance, dataset_path, file_names, file_to_table_map):
        # Initialize the base class (DataBase) with the database connection details
        super().__init__(db_instance.host, db_instance.database_name, db_instance.username, db_instance.password, db_instance.port, db_instance.tables)
        
        # Store the dataset path, file names, and the mapping from files to table names
        self.dataset_path = dataset_path
        self.file_names = file_names
        self.file_to_table_map = file_to_table_map
        
        # Create a connection string for the SQLAlchemy engine
        connection_string = f"mysql+mysqlconnector://{db_instance.username}:{db_instance.password}@{db_instance.host}:{db_instance.port}/{db_instance.database_name}"
        self.engine = create_engine(connection_string)

    def insert_csv_data(self):
        # Check if the SQLAlchemy engine has been initialized
        if self.engine is None:
            print("Engine has not been initialized!!")
            return
        
        # Create a dictionary with column names for each file based on the table definitions
        column_names = {file_name: [col[0] for col in self.tables[self.file_to_table_map[file_name]]] for file_name in self.file_names}

        # Dictionary to store the dataframes for each CSV file
        dataframes = {}

        # Loop through each file name
        for file_name in self.file_names:
            # Construct the full path to the CSV file
            csv_path = f'{self.dataset_path}/{file_name}'
            
            # Open the CSV file and read the first line to determine the number of columns
            with open(csv_path, 'r') as csvfile:
                first_line = csvfile.readline()
                num_columns_in_csv = len(first_line.split(','))
            
            # Determine the columns to use based on the number of columns in the CSV
            cols_to_use = column_names[file_name][:num_columns_in_csv] if num_columns_in_csv <= len(column_names[file_name]) else column_names[file_name]
            
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_path, names=cols_to_use, header=0)
            
            # Get the table name from the file-to-table mapping
            table_name = self.file_to_table_map[file_name]
            
            # Write the DataFrame to the SQL table
            df.to_sql(name=table_name, con=self.engine, if_exists='replace', index=False)
            print(f'Data Copied to {table_name} in SQL')
            
            # Store the DataFrame in the dataframes dictionary, using the file name without the extension as the key
            name_key = file_name.replace('.csv', '')
            dataframes[name_key] = df

    def get_csv_data(self, table_name):
        # Check if the SQLAlchemy engine has been initialized
        if not self.engine:
            print("Error: Database connection not established.")
            return None
        
        try:
            # Read the SQL table into a pandas DataFrame and return it
            return pd.read_sql_table(table_name, con=self.engine)
        except Exception as e:
            # Print and return the error if reading the SQL table fails
            print(f"Error reading data from {table_name}: {e}")
            return f"Error reading data from {table_name}: {e}"
