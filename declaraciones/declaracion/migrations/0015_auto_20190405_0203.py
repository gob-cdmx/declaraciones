# Generated by Django 2.2 on 2019-04-05 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declaracion', '0014_auto_20190405_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inversiones',
            name='plazo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True),
        ),
    ]
