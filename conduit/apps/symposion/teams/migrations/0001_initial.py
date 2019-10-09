# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('state', models.CharField(max_length=20, choices=[('applied', 'applied'), ('invited', 'invited'), ('declined', 'declined'), ('rejected', 'rejected'), ('member', 'member'), ('manager', 'manager')], verbose_name='State')),
                ('message', models.TextField(blank=True, verbose_name='Message')),
            ],
            options={
                'verbose_name_plural': 'Memberships',
                'verbose_name': 'Membership',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('access', models.CharField(max_length=20, choices=[('open', 'open'), ('application', 'by application'), ('invitation', 'by invitation')], verbose_name='Access')),
                ('created', models.DateTimeField(editable=False, default=datetime.datetime.now, verbose_name='Created')),
                ('manager_permissions', models.ManyToManyField(related_name='manager_teams', blank=True, to='auth.Permission', verbose_name='Manager permissions')),
                ('permissions', models.ManyToManyField(related_name='member_teams', blank=True, to='auth.Permission', verbose_name='Permissions')),
            ],
            options={
                'verbose_name_plural': 'Teams',
                'verbose_name': 'Team',
            },
        ),
        migrations.AddField(
            model_name='membership',
            name='team',
            field=models.ForeignKey(verbose_name='Team', to='teams.Team', related_name='memberships'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL, related_name='memberships'),
        ),
    ]
