# Generated by Django 4.2.13 on 2024-05-18 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0072_cell_value_normalized'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='use_normalized',
            field=models.BooleanField(default=False),
        ),
    ]
