# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='Name', help_text='As you would like it to appear in the conference program.', max_length=100)),
                ('biography', models.TextField(verbose_name='Biography', blank=True, help_text="A little bit about you.  Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/target='_blank'>Markdown</a>.")),
                ('biography_html', models.TextField(blank=True)),
                ('photo', models.ImageField(verbose_name='Photo', upload_to='speaker_photos', blank=True)),
                ('annotation', models.TextField(verbose_name='Annotation')),
                ('invite_email', models.CharField(verbose_name='Invite_email', unique=True, db_index=True, max_length=200, null=True)),
                ('invite_token', models.CharField(verbose_name='Invite token', db_index=True, max_length=40)),
                ('created', models.DateTimeField(editable=False, verbose_name='Created', default=datetime.datetime.now)),
                ('user', models.OneToOneField(null=True, related_name='speaker_profile', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Speaker',
                'verbose_name_plural': 'Speakers',
                'ordering': ['name'],
            },
        ),
    ]
