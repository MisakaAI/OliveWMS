# Generated by Django 4.2.1 on 2023-05-25 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0006_box'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='max_column',
            field=models.CharField(max_length=20, verbose_name='每层储位数'),
        ),
        migrations.AlterField(
            model_name='box',
            name='max_row',
            field=models.CharField(max_length=20, verbose_name='层数'),
        ),
    ]
