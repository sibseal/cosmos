# Generated by Django 5.0.2 on 2024-02-27 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_values'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Variant',
            new_name='Condition',
        ),
        migrations.RenameField(
            model_name='condition',
            old_name='product',
            new_name='task',
        ),
    ]