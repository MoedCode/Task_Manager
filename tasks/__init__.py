import csv
import os
from rest_framework import status as S


TASKS = []

from .csv_storage import CsvStorage
from .models import *

tasks_stor = CsvStorage(file_name="Tasks.csv",mode='w', clm_names=Tasks.KEYS)
tasks_stor.reload()

users_stor = CsvStorage(file_name="Users.csv", mode='w', clm_names=Users.KEYS)
users_stor.reload()
S200 = S.HTTP_200_OK
S201 = S.HTTP_201_CREATED
S304 = S.HTTP_304_NOT_MODIFIED
S400 = S.HTTP_400_BAD_REQUEST
S401 = S.HTTP_401_UNAUTHORIZED
S405 = S.HTTP_405_METHOD_NOT_ALLOWED
S403 = S.HTTP_403_FORBIDDEN
S404 = S.HTTP_404_NOT_FOUND
S422 = S.HTTP_422_UNPROCESSABLE_ENTITY