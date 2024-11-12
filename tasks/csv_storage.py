

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
        print(f"\n\n\n ------------   -------------- \n\n\n")
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

    def get_by(self, key=None, value=None):
        if not key or not value:
            return False, f"messing {'key' if key is None else ''} {'value' if value is None else ''}"
        if key not in self.clm_names:
            return False, f"key {key} not match"
        self.reload()
        for idx, task in enumerate(self.session):
            print(f"key : {key} value : {value}")

            if task[key] == value:
                return True, task, idx
        return False, f"{key} : {value} not found "
    def delete(self, key=None, value=None):
        res = self.get_by(key=key, value=value)
        if not res[0]:
            return  res[0], res[1]
        self.session.pop(res[2])
        self.save()

    def multi_selection(self, select_by=None, val_lst=[], action="get"):
        if not select_by or not len(val_lst) or select_by not in self.clm_names:
            msg = f"{' -empty list.' if not  len(val_lst) else '' }"
            msg += f"{'-No key to select by' if not  select_by else ''}"
            msg += f"-{select_by} Not A valid Key" if select_by not in self.clm_names else ""
            return False, msg
        self.reload()
        selected_tasks = []
        indexes = []
        for val in val_lst:
            for index, task in enumerate(self.session):
                if task[select_by] == val:
                    indexes.append(index)
                    selected_tasks.append(task)
        if not len(selected_tasks):
            return False, f"No Result Match {val_lst}"
        if action == "get":
            return True, selected_tasks, indexes
        if action == "delete":
            for index in indexes:
                self.session.pop(index)
                self.save()