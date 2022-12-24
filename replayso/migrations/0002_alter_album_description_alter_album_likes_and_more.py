# Generated by Django 4.1.3 on 2022-11-22 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('replayso', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.TextField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='album',
            name='likes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='artist',
            name='description',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='artist',
            name='listeners',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='track',
            name='likes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='track',
            name='plays',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='track',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]