# Generated by Django 4.2.2 on 2023-06-21 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_rename_ratingauthor_author_ratingauthor'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='data',
            field=models.DateField(default='2023-01-01'),
        ),
    ]
