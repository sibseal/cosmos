# Generated by Django 5.0.2 on 2024-04-09 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_rename_condition_criterion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='method',
            name='control_sum_of_criteria',
            field=models.BooleanField(default=False),
        ),
    ]