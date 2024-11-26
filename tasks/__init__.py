import csv
import os
import inspect

from rest_framework import status as S


TASKS = []

from tasks.csv_storage import CsvStorage
from tasks.models import *

def DEBUG(format="", linChar=""):
    # Get the current frame
    frame = inspect.currentframe()
    # Get the caller's frame (where DEUG is called)
    caller_frame = frame.f_back
    # Extract file name and line number
    file_name = os.path.basename(caller_frame.f_code.co_filename)
    line_number = caller_frame.f_lineno
    # Return formatted string
    print( f"{file_name}, line {line_number} ::{linChar} {format}")


tasks_stor = CsvStorage(file_name="Tasks.csv",mode='w', pair_class=Tasks)
tasks_stor.reload()
# DEBUG(f'{ tasks_stor.search("task", {"method":"startwith", "value":"__"})} ')
DEBUG(f'{ tasks_stor.get_columns(["task", "user_id"], True)} ')
users_stor = CsvStorage(file_name="Users.csv", mode='w', pair_class=Users)
users_stor.reload()

tokens_stor = CsvStorage(file_name="Auth.csv", mode='w', pair_class=Tokens)
tokens_stor.reload()
Storages = {"tasks":tasks_stor, "users":users_stor, "auth":tokens_stor}
Storages_keys = list(Storages.keys())
Classes  = {"tasks":Tasks, "users":Users, "auth":tokens_stor}
S200 = S.HTTP_200_OK
S201 = S.HTTP_201_CREATED
S304 = S.HTTP_304_NOT_MODIFIED
S400 = S.HTTP_400_BAD_REQUEST
S401 = S.HTTP_401_UNAUTHORIZED
S405 = S.HTTP_405_METHOD_NOT_ALLOWED
S403 = S.HTTP_403_FORBIDDEN
S404 = S.HTTP_404_NOT_FOUND
S422 = S.HTTP_422_UNPROCESSABLE_ENTITY


