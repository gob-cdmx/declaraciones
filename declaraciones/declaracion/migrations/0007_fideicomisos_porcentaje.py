# Generated by Django 2.2 on 2019-04-03 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declaracion', '0006_fideicomisos_nombre_fideicomiso'),
    ]

    operations = [
        migrations.AddField(
            model_name='fideicomisos',
            name='porcentaje',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
