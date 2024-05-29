import pandas as pd
import numpy as np

class Calculations:
    def __init__(self, df_train, df_ideal, df_test):
        self.df_train = df_train
        self.df_ideal = df_ideal
        self.df_test = df_test
        self.best_ideal_functions = []
        self.sqrt_max_deviation = {}
        self.test_results = []

    def calc_ssd_sums(self):
        ssd_sums = {}
        for j in range(1, 5):
            ssd_sums_each = {}
            for i in range(1, 51):
                col_name = f'Y{i} (ideal func)'
                if col_name in self.df_ideal.columns:  # Check if the column exists
                    ssd = ((self.df_train.iloc[:, j] - self.df_ideal[col_name])**2).sum()
                    ssd_sums_each[col_name] = ssd
                else:
                    print(f"Column '{col_name}' not found in df_ideal.")
            ssd_sums[f'Y{j} (training func)'] = ssd_sums_each
            top_func = sorted(ssd_sums_each, key=ssd_sums_each.get)[0] if ssd_sums_each else None
            self.best_ideal_functions.append(top_func)
        print("Best ideal functions are:", self.best_ideal_functions)
        return ssd_sums


    def calc_deviations(self):
        best_ideal_functions = [func for func in self.best_ideal_functions if func]  # Filter out None values
        training_function_columns = ['Y1 (training func)', 'Y2 (training func)', 'Y3 (training func)', 'Y4 (training func)']

        max_deviations = {}
        for ideal_func in best_ideal_functions:
            if ideal_func in self.df_ideal.columns:  # Check if the column exists
                all_deviations = [np.abs(self.df_train[train_func] - self.df_ideal[ideal_func]) for train_func in training_function_columns]
                combined_deviations = np.concatenate(all_deviations)
                max_deviations[ideal_func] = np.max(combined_deviations)
            else:
                print(f"Column '{ideal_func}' not found in df_ideal.")

        self.sqrt_max_deviation = {func: deviation * np.sqrt(2) for func, deviation in max_deviations.items()}


    def get_best_fit(self,x_val, y_val, chosen_functions, df_ideal, sqrt_max_deviation):
        best_fit_ideal_function = {'func': None, 'deviation': np.inf}
        for func in chosen_functions:
            ideal_y_val = df_ideal.loc[df_ideal['X'] == x_val, func].iloc[0]
            deviation = np.abs(ideal_y_val - y_val)
            if deviation < sqrt_max_deviation[func] and deviation < best_fit_ideal_function['deviation']:
                best_fit_ideal_function = {'func': func, 'deviation': deviation}
        return best_fit_ideal_function

    def get_test_results(self):
        test_results=[]
        for _, row in self.df_test.iterrows():
            match = self.get_best_fit(row['X (test func)'], row['Y (test func)'], self.best_ideal_functions, self.df_ideal, self.sqrt_max_deviation)
            test_results.append({
                'X (test func)': row['X (test func)'],
                'Y (test func)': row['Y (test func)'],
                'Delta Y (test func)': match['deviation'] if match['func'] else None,
                'No. of ideal func': match['func']
            })
        return test_results
