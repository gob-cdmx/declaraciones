# Generated by Django 2.2 on 2019-04-05 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declaracion', '0013_merge_20190404_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deudasotros',
            name='plazo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='inversiones',
            name='plazo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]