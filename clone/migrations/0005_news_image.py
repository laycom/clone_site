# Generated by Django 3.1 on 2020-09-03 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clone', '0004_news_descriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(null=True, upload_to='media/article/'),
        ),
    ]