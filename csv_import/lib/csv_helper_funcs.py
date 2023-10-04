from csv_import.models.upload_contents import *
from datetime import datetime
from csv_import.models import *
import csv


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
    # could use pandas but reinventing the wheel is better
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