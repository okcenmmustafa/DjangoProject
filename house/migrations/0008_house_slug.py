# Generated by Django 3.0.4 on 2020-05-05 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0007_auto_20200505_0408'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
