# Generated by Django 3.0.4 on 2020-05-05 01:08

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0006_auto_20200330_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
