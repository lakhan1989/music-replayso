# Generated by Django 4.1.3 on 2022-11-25 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('replayso', '0002_alter_album_description_alter_album_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='description',
            field=models.TextField(max_length=200),
        ),
    ]
