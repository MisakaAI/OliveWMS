# Generated by Django 4.2.1 on 2023-05-25 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0002_item_alter_supplier_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='价格'),
        ),
    ]
