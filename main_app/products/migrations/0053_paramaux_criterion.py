# Generated by Django 5.0.2 on 2024-05-12 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0052_alter_param_single'),
    ]

    operations = [
        migrations.AddField(
            model_name='paramaux',
            name='criterion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.criterion'),
        ),
    ]
