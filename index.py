from db import DataBase
from process_csv import ProcessCsv
from calculation import Calculations
from plotting import Plot

class MainProcess:
    def __init__(self, host, database_name, username, password, port, tables, dataset_path, file_names, file_to_table_map):
        self.host = host
        self.database_name = database_name
        self.username = username
        self.password = password
        self.port = port
        self.tables = tables
        self.dataset_path = dataset_path
        self.file_names = file_names
        self.file_to_table_map = file_to_table_map

    def run(self):
        # Step 1: Create the database and tables
        
        db_instance = DataBase(self.host, self.database_name, self.username, self.password, self.port, self.tables)
        db_instance.create_database()
        db_instance.create_tables()
        db_instance.close_connection()

        # Step 2: Read CSV files and load data into the database using ProcessCsv which inherits DataBase
        csv_instance = ProcessCsv(db_instance, self.dataset_path, self.file_names, self.file_to_table_map)
        csv_instance.insert_csv_data()

        # Step 3: Read data from SQL tables
        df_train = csv_instance.get_csv_data('train_functions')
        df_ideal = csv_instance.get_csv_data('ideal_functions')
        df_test = csv_instance.get_csv_data('test_functions')

        # Step 4: Perform calculations
        calc_instance = Calculations(df_train, df_ideal, df_test)
        ssd_sums = calc_instance.calc_ssd_sums()
        calc_instance.calc_deviations()
        test_results = calc_instance.get_test_results()

        # Step 5: Plot results
        plot_instance = Plot(ssd_sums, test_results)
        plot_instance.plotting()

if __name__ == "__main__":
    host = '127.0.0.1'
    database_name = 'py_db'
    username = 'root'
    password = 'root'
    port = 3306

    tables = {
        "train_functions": [('X', 'FLOAT'), ('Y1 (training func)', 'FLOAT'), ('Y2 (training func)', 'FLOAT'), ('Y3 (training func)', 'FLOAT'), ('Y4 (training func)', 'FLOAT')],
        "test_functions": [('X (test func)', 'FLOAT'), ('Y (test func)', 'FLOAT'), ('Delta Y (test func)', 'FLOAT'), ('No. of ideal func', 'VARCHAR(255)')],
        "ideal_functions": [('X', 'FLOAT')] + [(f'Y{i} (ideal func)', 'FLOAT') for i in range(1, 51)],
    }

    file_names = ['train.csv', 'test.csv', 'ideal.csv']
    dataset_path = './Csv files/'
    file_to_table_map = {'train.csv': 'train_functions', 'test.csv': 'test_functions', 'ideal.csv': 'ideal_functions'}

    main_process = MainProcess(host, database_name, username, password, port, tables, dataset_path, file_names, file_to_table_map)
    main_process.run()

