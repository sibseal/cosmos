# Generated by Django 4.2.13 on 2024-05-18 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0071_task_changed'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='value_normalized',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]