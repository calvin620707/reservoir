# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='costrecord',
            name='sheets_cost_project_8cabe8_idx',
        ),
        migrations.RemoveIndex(
            model_name='costrecord',
            name='sheets_cost_project_c57fc5_idx',
        ),
        migrations.AddField(
            model_name='costrecord',
            name='category',
            field=models.CharField(choices=[('FO', 'Food'), ('CL', 'Clothing'), ('HO', 'Housing'), ('TR', 'Transportation'), ('ED', 'Education'), ('EN', 'Entertainment'), ('OT', 'Others')], default='OT', max_length=2),
        ),
    ]