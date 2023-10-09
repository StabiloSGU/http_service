from csv_import.models.upload_contents import *
from datetime import datetime
from csv_import.models import *
from django.db.models import F
import csv
import pandas as pd
import numpy as np

def parse_csv_to_database(file_id) -> None:
    file = Upload.objects.get(pk=file_id)
    filepath = file.file.path
    with open(filepath, newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.readline(), delimiters=",;")
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        headers = []
        for i, row in enumerate(reader):
            if i == 0:
                for header in row:
                    new_field = UploadContentsFields(file=file, name=header)
                    new_field.save()
                    headers.append(new_field)
            else:
                for j, val in enumerate(row):
                    new_value = UploadContentsFieldValues(field=headers[j], row_num=i, value=val)
                    new_value.save()

def determine_type(val):
    types = (
        (int, int),
        (float, float),
        (datetime, lambda x: datetime.strptime(x, "%d.%M.%Y")),
    )

    for comparable_type, test_value in types:
        try:
            test_value(val)
            return comparable_type
        except ValueError:
            continue
    return str

def get_file_column_info(file_pk: int, row_number: int = 2) -> tuple:
    file_obj = Upload.objects.get(pk=file_pk)
    headers = UploadContentsFields.objects.filter(file=file_obj)
    header_names = (header.name for header in headers)
    column_types = []
    row_values = []
    for header in headers:
        cell = UploadContentsFieldValues.objects.get(field=header, row_num=row_number)
        column_types.append(determine_type(cell.value).__name__)
        row_values.append(cell.value)
    return (header_names, column_types,row_values)


def get_df_from_file_using_database(file_pk: int):
    file = Upload.objects.get(pk=file_pk)
    headers = UploadContentsFields.objects.filter(file=file)
    data = {}
    for header in headers:
        field_values_column = UploadContentsFieldValues.objects.filter(field=header).order_by(F("row_num").asc())
        column = [cell.value for cell in field_values_column]
        data[header.name] = column
    df = pd.DataFrame(data)
    return df

def get_df_from_file_using_pandas(file_pk: int):
    file_path = Upload.objects.get(pk=file_pk).file.path
    df = pd.read_csv(file_path)
    return df

def determine_upload_method(file_pk: int) -> int:
    file = Upload.objects.get(pk=file_pk)
    if UploadContentsFields.objects.filter(file=file.pk).exists():
        return ImportSettings.DB
    else:
        return ImportSettings.PANDAS


def get_file_column_info_using_pandas(file_pk: int, row_number = 0) -> tuple:
    file_path = Upload.objects.get(pk=file_pk).file.path
    df = pd.read_csv(file_path)
    header_names = (header for header in df.columns)
    column_types = []
    row_values = []
    for cell in df.iloc[row_number]:
        column_types.append(type(cell).__name__)
        row_values.append(cell)
    return (header_names, column_types,row_values)

def convert_df_to_dict(df: pd.DataFrame) -> dict:
    header_names = [header for header in df.columns]
    df_len = len(df.index)
    to_np_array = df.to_numpy()
    rows = to_np_array.reshape(df_len, len(df.columns))
    return {"headers": header_names, "rows": rows}
