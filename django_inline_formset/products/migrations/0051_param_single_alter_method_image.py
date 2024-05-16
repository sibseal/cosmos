# Generated by Django 5.0.2 on 2024-05-12 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0050_remove_method_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='param',
            name='single',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='method',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
