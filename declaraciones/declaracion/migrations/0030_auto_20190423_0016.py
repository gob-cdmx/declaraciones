# Generated by Django 2.2 on 2019-04-23 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declaracion', '0029_conyugedependientes_otra_relacion_familiar'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiosespecie',
            name='otra_relacion_familiar',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='bienespersonas',
            name='otra_relacion_familiar',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='otraspartes',
            name='otra_relacion_familiar',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]