# Generated by Django 5.0.2 on 2024-02-26 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_item_probability'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variant',
            old_name='size',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='price',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='quantity',
        ),
        migrations.AddField(
            model_name='variant',
            name='value',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Probability',
        ),
    ]
