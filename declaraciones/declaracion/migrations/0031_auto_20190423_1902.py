# Generated by Django 2.2 on 2019-04-23 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declaracion', '0030_auto_20190423_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaraciones',
            name='fecha_declaracion',
            field=models.DateField(null=True,auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='secciones',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='secciones',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='secciones',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
