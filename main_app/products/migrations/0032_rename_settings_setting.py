# Generated by Django 5.0.2 on 2024-04-21 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_settings_alter_method_description_alter_method_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Settings',
            new_name='Setting',
        ),
    ]
