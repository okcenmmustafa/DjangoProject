# Generated by Django 3.0.4 on 2020-05-14 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0015_auto_20200515_0144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='houseType',
        ),
        migrations.DeleteModel(
            name='houseType',
        ),
    ]
