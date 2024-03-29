# Generated by Django 2.2 on 2019-04-05 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('declaracion', '0016_auto_20190405_0208'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatCamposObligatorios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tabla', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_columna', models.CharField(blank=True, max_length=255, null=True)),
                ('es_obligatorio', models.IntegerField(blank=True, null=True)),
                ('seccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='declaracion.Secciones')),
            ],
        ),
    ]
