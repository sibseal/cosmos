# Generated by Django 5.0.2 on 2024-02-26 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_rename_size_variant_name_remove_variant_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='short_description',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
