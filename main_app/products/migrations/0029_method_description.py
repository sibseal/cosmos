# Generated by Django 5.0.2 on 2024-04-10 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0028_task_methods'),
    ]

    operations = [
        migrations.AddField(
            model_name='method',
            name='description',
            field=models.CharField(default='', max_length=10000),
            preserve_default=False,
        ),
    ]