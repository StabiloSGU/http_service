# Generated by Django 4.2.5 on 2023-10-02 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_import', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='file',
            field=models.FileField(upload_to='csv_import/uploads/'),
        ),
    ]
