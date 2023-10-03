from csv_import.models.upload_contents import *
import csv


def parse_csv_to_database(file_id):
    file = Upload.objects.get(pk=file_id)
    filepath = file.file.path
    with open(filepath, newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
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
                print('headers', headers)
                for j, val in enumerate(row):
                    new_value = UploadContentsFieldValues(field=headers[j], row_num=i, value=val)
                    new_value.save()
