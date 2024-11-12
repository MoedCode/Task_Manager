import csv
import os
from rest_framework import status as S


TASKS = []

from .csv_storage import CsvStorage
csv_stor = CsvStorage(mode='w')
csv_stor.clm_names = ["task", "priority", "kickoff", "id", "username", "created", "updated"]
csv_stor.reload()

S200 = S.HTTP_200_OK
S201 = S.HTTP_201_CREATED
S304 = S.HTTP_304_NOT_MODIFIED
S400 = S.HTTP_400_BAD_REQUEST
S401 = S.HTTP_401_UNAUTHORIZED
S405 = S.HTTP_405_METHOD_NOT_ALLOWED
S403 = S.HTTP_403_FORBIDDEN
S404 = S.HTTP_404_NOT_FOUND
S422 = S.HTTP_422_UNPROCESSABLE_ENTITY