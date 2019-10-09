# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('start_date', models.DateField(null=True, blank=True, verbose_name='Start date')),
                ('end_date', models.DateField(null=True, blank=True, verbose_name='End date')),
                ('timezone', timezone_field.fields.TimeZoneField(blank=True, verbose_name='timezone')),
            ],
            options={
                'verbose_name_plural': 'conferences',
                'verbose_name': 'conference',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('start_date', models.DateField(null=True, blank=True, verbose_name='Start date')),
                ('end_date', models.DateField(null=True, blank=True, verbose_name='End date')),
                ('conference', models.ForeignKey(to='symposion_conference.Conference', verbose_name='Conference')),
            ],
            options={
                'ordering': ['start_date'],
                'verbose_name_plural': 'sections',
                'verbose_name': 'section',
            },
        ),
    ]
