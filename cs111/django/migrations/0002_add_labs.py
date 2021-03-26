# Generated by Django 3.1.7 on 2021-03-26 17:18

import cs111.django.storages
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs111', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('pdf', models.FileField(storage=cs111.django.storages.OverwriteFileSystemStorage, upload_to='cs111/labs')),
            ],
        ),
    ]
