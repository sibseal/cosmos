# Generated by Django 5.0.2 on 2024-04-21 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0032_rename_settings_setting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setting',
            old_name='max_item',
            new_name='max_items',
        ),
    ]