# Generated by Django 5.0.2 on 2024-02-27 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_book_task_books_delete_choice_delete_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condition',
            name='user',
        ),
        migrations.RemoveField(
            model_name='item',
            name='user',
        ),
        migrations.RemoveField(
            model_name='task',
            name='books',
        ),
    ]
