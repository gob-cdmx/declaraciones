# Generated by Django 2.2 on 2019-04-08 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('declaracion', '0020_auto_20190408_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membresias',
            name='tiene_apoyos',
        ),
    ]
