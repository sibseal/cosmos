# Generated by Django 5.0.2 on 2024-05-04 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_methodparam_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterion',
            name='name_short',
            field=models.CharField(default='', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='name_short',
            field=models.CharField(default='', max_length=5),
            preserve_default=False,
        ),
    ]
