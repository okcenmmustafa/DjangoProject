# Generated by Django 3.0.4 on 2020-05-24 16:11

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20200524_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
