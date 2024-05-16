# Generated by Django 5.0.2 on 2024-02-27 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_rename_title_task_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Values',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.item')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.task')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variant')),
            ],
        ),
    ]
