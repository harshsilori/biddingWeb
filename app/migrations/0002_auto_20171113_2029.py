# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-11-13 14:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='bid',
        ),
        migrations.RemoveField(
            model_name='items',
            name='owner',
        ),
    ]