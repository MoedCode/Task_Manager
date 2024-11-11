import csv
import os


TASKS = []

from .csv_storage import CsvStorage
csv_stor = CsvStorage(mode='w')
csv_stor.clm_names = ["task", "priority", "kickoff", "id"]
csv_stor.reload()