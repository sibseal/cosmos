# Generated by Django 5.0.2 on 2024-02-27 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_rename_product_item_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='values',
            old_name='variant',
            new_name='condition',
        ),
    ]
