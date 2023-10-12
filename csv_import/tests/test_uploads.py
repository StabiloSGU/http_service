from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from csv_import.forms import UploadForm
from csv_import.models import *

import os


class UploadUsingPandasTest(TestCase):
    TEST_FILES_FOLDER = 'test_csv_files'
    APP_NAME = 'csv_import'
    UPLOADS_FOLDER = 'uploads'

    def setUp(self):
        self.uploads_dir_path = os.path.abspath(os.path.join(UploadUsingPandasTest.APP_NAME,
                                                             UploadUsingPandasTest.UPLOADS_FOLDER))
        self.test_files_folder_path = os.path.abspath(os.path.join(UploadUsingPandasTest.APP_NAME,
                                                                   UploadUsingPandasTest.TEST_FILES_FOLDER))
        self.filelist = [f for f in os.listdir(self.test_files_folder_path)\
                         if os.path.isfile(os.path.join(self.test_files_folder_path, f))]
        self.files_created_during_test = []

    def test_uploading_with_form(self):
        for filename in self.filelist:
            with self.subTest(filename=filename):
                filepath = os.path.join(self.test_files_folder_path, filename)
                f = File(open(filepath, 'rb')).read()
                data = {
                    'name': filename,
                    'upload_choice': ImportSettings.PANDAS,
                }
                files = {
                    'file': SimpleUploadedFile(name=f'testcase_{filename}', content=f, content_type='multipart/form-data'),
                    }
                upload_form = UploadForm(data=data, files=files)
                self.assertTrue(upload_form.is_valid())

                new_upload = upload_form.save()
                head, tail = os.path.split(new_upload.file.path)
                self.files_created_during_test.append(tail)

    def tearDown(self):
        for filename in self.files_created_during_test:
            os.remove(os.path.join(self.uploads_dir_path, filename))
