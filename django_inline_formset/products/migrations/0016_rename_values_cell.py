# Generated by Django 5.0.2 on 2024-02-27 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_remove_condition_user_remove_item_user_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Values',
            new_name='Cell',
        ),
    ]
