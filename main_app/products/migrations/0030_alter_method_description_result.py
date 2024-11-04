# Generated by Django 5.0.2 on 2024-04-21 11:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_method_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='method',
            name='description',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='result_item', to='products.item')),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='result_method', to='products.method')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='result_task', to='products.task')),
            ],
        ),
    ]