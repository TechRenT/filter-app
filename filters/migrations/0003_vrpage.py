# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-03-22 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0002_filter_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='VRPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]