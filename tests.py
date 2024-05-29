import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from index import MainProcess  # Assuming the class is in a file named main_process.py
from db import DataBase
from process_csv import ProcessCsv
from calculation import Calculations
from plotting import Plot

class TestMainProcess(unittest.TestCase):

    @patch('db.DataBase')
    @patch('process_csv.ProcessCsv')
    @patch('calculation.Calculations')
    @patch('plotting.Plot')
    def test_run(self, MockPlot, MockCalculations, MockProcessCsv, MockDataBase):
        # Set up mock instances
        mock_db_instance = MockDataBase.return_value
        mock_csv_instance = MockProcessCsv.return_value
        mock_calc_instance = MockCalculations.return_value
        mock_plot_instance = MockPlot.return_value

        # Mock the return values for CSV data retrieval
        df_train = pd.DataFrame({'X': [1, 2], 'Y1 (training func)': [3, 4]})
        df_ideal = pd.DataFrame({'X': [1, 2], 'Y1 (ideal func)': [3, 4]})
        df_test = pd.DataFrame({'X (test func)': [1, 2], 'Y (test func)': [3, 4]})

        mock_csv_instance.get_csv_data.side_effect = lambda table_name: {
            'train_functions': df_train,
            'ideal_functions': df_ideal,
            'test_functions': df_test
        }[table_name]

        # Mock the calculations
        ssd_sums = {'sum_squares': 10}
        test_results = {'test_result': [1, 2, 3]}
        mock_calc_instance.calc_ssd_sums.return_value = ssd_sums
        mock_calc_instance.get_test_results.return_value = test_results

        # Initialize MainProcess with test parameters
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

if __name__ == '__main__':
    unittest.main()
