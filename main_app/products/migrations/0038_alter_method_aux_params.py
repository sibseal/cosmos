# Generated by Django 5.0.2 on 2024-05-04 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_method_need_criterion_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='method',
            name='aux_params',
            field=models.ManyToManyField(blank=True, to='products.methodparam'),
        ),
    ]