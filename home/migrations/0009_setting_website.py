# Generated by Django 3.0.4 on 2020-05-16 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='website',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
