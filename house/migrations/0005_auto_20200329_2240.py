# Generated by Django 3.0.4 on 2020-03-29 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0004_auto_20200329_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=90),
        ),
        migrations.AlterField(
            model_name='house',
            name='title',
            field=models.CharField(max_length=90),
        ),
    ]
