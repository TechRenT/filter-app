# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-11-29 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0006_remove_linkedinprofile_checker'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcepTld',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tld', models.CharField(max_length=15)),
            ],
        ),
    ]
