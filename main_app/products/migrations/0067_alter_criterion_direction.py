# Generated by Django 4.2.13 on 2024-05-15 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0066_cell_changed_celldescartescriterion_changed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterion',
            name='direction',
            field=models.BooleanField(default=False),
        ),
    ]