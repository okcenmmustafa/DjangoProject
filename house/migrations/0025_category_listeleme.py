# Generated by Django 3.0.4 on 2020-05-17 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0024_auto_20200516_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='listeleme',
            field=models.IntegerField(default=0, max_length=10),
        ),
    ]
