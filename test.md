complete this method   to can search for in csv file , i will use it as follow
```py
tasks_stor.search(query_data={"method":"startwith", "query":{"task":"__", "user_id":"0d9e6101-0988-4198-9768-298a1f400474"}})
```
it should return all tasks with user id ` 0d9e6101-0988-4198-9768-298a1f400474`
that start  with `__`
query  method can be `contain`  or `identical` for identical  result
i my be male case sensitive
also i cam make `query ` more thant to key and tow value
method need to corrected
```py
    def search(self,  query_data:Dict = {}) -> Union[List[Dict], Dict]:
        """
        search - Searches for rows in a dataset that match the given criteria.
        Args:
        column_name: (str) The name of the column to search in. Defaults to an empty string.
        query_data: (dict) Key-value pairs to filter rows by. Supports nested dictionaries. Defaults to an empty dictionary.
        Return:
            - List[Dict]: A list of dictionaries representing matching rows, if successful.
            - Dict: A dictionary containing error information, if an error occurs.
        """
        # handling potential issues
        error_msg = ""
        if not  query_data or not isinstance(query_data, dict): error_msg += "No data to filter,  "
        # get search method  search keys"column names"" and values
        query = query_data.get("query", {})
        method = query_data.get("method", "")
        keys , values = list(query.keys()) , list(query.values())
        if not  query_data["method"]: error_msg += "No valid method to filter, "
        if not  query : error_msg += "No valid query to filter, "
        if  not keys or not values:
            error_msg += f"query must be dict for key and values, keys:{keys} , values:{values} "
        if error_msg:
            return [False, {"Error":error_msg}]
        # query all column
        columns = self.get_columns(keys, True)

        if ("case_sens", "case_sensitive", ) in query_data:
            case_sens = query_data["case_sens"] or query_data["case_sensitive"]
        else: case_sens = False
        # get search keys
        # get columns crossponding to search values
        # header = columns.pop(0)
        result_dict = {}

        col_len = len(columns["header"])
        del columns["header"]
        for key, clm_values in columns.items():
            result_dict[key] = []
            for clm_value in clm_values:
                DEBUG(f"clm_value {clm_value },: {type(clm_value)}")
                if clm_value and clm_value.startswith(query[key]):
                    result_dict[key].append(clm_value)
        return result_dict
        if not case_sens :
            values = [value.lower() for value in values]
            columns = [[el.lower() for el in column] for column in  columns]
        if method in  ("start_with", "start with", "startwith"):
            matching_result = []
            # for value in
        # for i in range(len jeys)
```
methods you can use
Note you get_column handle empty rows
```py
    def reader(self):
        try:
            file = open(self.file_path, mode='r')  # Open the file
            reader = csv.reader(file)  # Use the file
            return  file, reader
        except Exception as e:
            raise e
    def get_columns(self, columns_names: str = "", map:bool = False) -> List[str]:
        """
        Get one or more CSV columns by their names.
        Args:
            columns_names (str): The name(s) of the column(s) to retrieve
        Returns:
            List[str]: The values in the specified column(s).
        """
        if isinstance(columns_names, str):
            columns_names = [columns_names]

        file, reader = self.reader()
        header = next(reader)  # Read the header row
        try:
            idxs = [header.index(name) for name in columns_names]
        except ValueError as e:
            file.close()
            return [False, str(ValueError(f"Column '{columns_names}' not found in CSV file."))]

        data = {name: [] for name in columns_names}  # Initialize a dict for results
        rows = list(reader)  # Convert reader to a list to allow multiple passes
        if not map:
            file.close()
            result = [header[:]]  # Initialize the result list

            # Iterate over each column index in idxs
            for idx in idxs:
                # For each column index, collect the values from rows
                column_data = [
                    row[idx] if idx < len(row) and row[idx] else None  # Check index and handle empty values
                    for row in rows
                ]
                result.append(column_data)  # Append the column data to the result
            return result


        for idx, name in zip(idxs, columns_names):
            data[name] = [
                row[idx] if idx < len(row) and row[idx] else None  # Check index and handle empty values
                for row in rows
            ] # Collect column values
        data["header"] = header[:]
        file.close()
        return data

```