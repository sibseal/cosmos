# Generated by Django 5.0.2 on 2024-04-09 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_alter_choice_methods'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='description',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]