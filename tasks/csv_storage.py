

import csv
import os
from collections import Counter
class CsvStorage():
    def __init__(self, file_name='output.csv', mode='a',line='', clm_names=[]) -> None:
        self.tasks_dir = os.path.dirname(__file__)  # Gets the directory of the current file (tasks)
        self.file_path = os.path.join(self.tasks_dir, file_name)  # Build the full path within tasks
        self.line = line
        self.mode = mode
        self.session  = []
        self.clm_names = sorted(clm_names)
    def csv_read(self):


        data_list = []  # List to store each row as a dictionary

        try:
            with open(self.file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)  # Automatically uses header as keys
                for row in csv_reader:
                    # Append each row as-is (as a dictionary) to the data_list
                    data_list.append(dict(row))

            print("Data successfully read.")
            return data_list  # Return the list of dictionaries

        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    def reload(self):
        self.session =  self.csv_read()
        return len(self.session)
    def add(self, data):
        if not data or type(data) != dict:
            return False, f"{type(data)} .."
        data_k = sorted(list(data.keys()))
        if Counter(data_k) != Counter(self.clm_names):
            return False, f"Key  does not match \n {data_k}  self.cllm {self.clm_names}"
        self.session.append(data)
        return True, "task added successfully"
    def save(self):

        self.csv_write(self.session)
    def csv_write(self, data):

        # Build the path to save output.csv within the tasks directory

        try:
            # For debugging, print the absolute path where the file will be saved
            abs_path = os.path.abspath(self.file_path)
            print(f"Attempting to write to file at: {abs_path}")

            # Extract field names from the first dictionary in the data list
            fieldnames = self.clm_names

            with open(file=self.file_path, mode=self.mode, newline=self.line) as file:
                csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

                # Write header only if the file is being created or overwritten
                if self.mode == 'w':
                    csv_writer.writeheader()

                # Write the data rows
                csv_writer.writerows(data)

            print(f"\n\nData written successfully to {abs_path}\nDATA\n:{data}\n\n")

        except Exception as e:
            print(f"An error occurred: {e}")

