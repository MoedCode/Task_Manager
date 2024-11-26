```py

    def serve_html(self, filepath):
        """Serve an HTML file."""
        try:
            base_dir = os.path.dirname(__file__)
            abs_path = os.path.join(base_dir, filepath)
            print(f"{DEBUG()} >> \n base_dir[{base_dir}] \n abs_path[{abs_path}] \n filepath[{filepath}]")

            with open(abs_path, "rb") as file:
                self._set_headers(200, "text/html")
                self.wfile.write(file.read())
        except FileNotFoundError:
            self._set_headers(404, "text/html")
            self.wfile.write(b"<h1>404 Not Found</h1>")

```

```py
    def reader(self):
        f_path = self.file_path

        class Reader:
            def __init__(self, f_path=""):
                self.file = open(f_path, mode='r')  # Open the file
                self.reader = csv.reader(self.file)  # Use the file

            def close(self):
                self.file.close()

        return Reader(f_path)
    def get_column(self, col_name: str = "") -> List[str]:
        """
        Get a CSV column by its name.
        Args:
            col_name (str): The name of the column to retrieve
        Returns:
            List[str]: The values in the specified column.
    """
        x = self.reader()
        reader = x.reader
        # Get the header row and find the index of the column
        header = next(reader.reader)  # Read the first row (header)
        try:
            idx = header.index(col_name)  # Find index of the column
        except ValueError:
            return  ["Error", str(ValueError(f"Column '{col_name}' not found in CSV file."))]
        column = [row[idx] for row in reader]
        x.close()
        return column
```
```sh

mohamed@DESKTOP-S296B4S /mnt/c/Users/Active/Desktop/Coding/Gradutaion/simple_tasker
 % python3 tasks/__init__.py
Traceback (most recent call last):
  File "tasks/__init__.py", line 10, in <module>
    from tasks.csv_storage import CsvStorage
  File "/mnt/c/Users/Active/Desktop/Coding/Gradutaion/simple_tasker/tasks/__init__.py", line 27, in <module>
    DEBUG(f"{ tasks_stor.get_column('task')}")
  File "/mnt/c/Users/Active/Desktop/Coding/Gradutaion/simple_tasker/tasks/csv_storage.py", line 65, in get_column
    header = next(reader.reader)  # Read the first row (header)
AttributeError: '_csv.reader' object has no attribute 'reader'
mohamed@DESKTOP-S296B4S /mnt/c/Users/Active/Desktop/Coding/Gradutaion/simple_tasker
 %
```