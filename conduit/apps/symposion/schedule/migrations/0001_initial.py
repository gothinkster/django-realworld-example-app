# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_speakers', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('symposion_conference', '0001_initial'),
        ('symposion_proposals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='Date')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'date',
                'verbose_name_plural': 'dates',
            },
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('description_html', models.TextField(blank=True)),
                ('abstract', models.TextField(verbose_name='Abstract')),
                ('abstract_html', models.TextField(blank=True)),
                ('cancelled', models.BooleanField(default=False, verbose_name='Cancelled')),
                ('additional_speakers', models.ManyToManyField(related_name='copresentations', to='symposion_speakers.Speaker', verbose_name='Additional speakers', blank=True)),
                ('proposal_base', models.OneToOneField(to='symposion_proposals.ProposalBase', related_name='presentation', verbose_name='Proposal base')),
                ('section', models.ForeignKey(to='symposion_conference.Section', related_name='presentations', verbose_name='Section')),
            ],
            options={
                'ordering': ['slot'],
                'verbose_name': 'presentation',
                'verbose_name_plural': 'presentations',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=65, verbose_name='Name')),
                ('order', models.PositiveIntegerField(verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published', models.BooleanField(default=True, verbose_name='Published')),
                ('hidden', models.BooleanField(default=False, verbose_name='Hide schedule from overall conference view')),
                ('section', models.OneToOneField(to='symposion_conference.Section', verbose_name='Section')),
            ],
            options={
                'ordering': ['section'],
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.ForeignKey(to='symposion_schedule.Day', related_name='sessions', verbose_name='Day')),
            ],
            options={
                'verbose_name': 'Session',
                'verbose_name_plural': 'Sessions',
            },
        ),
        migrations.CreateModel(
            name='SessionRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.IntegerField(verbose_name='Role', choices=[(1, 'Session Chair'), (2, 'Session Runner')])),
                ('status', models.NullBooleanField(verbose_name='Status')),
                ('submitted', models.DateTimeField(default=datetime.datetime.now)),
                ('session', models.ForeignKey(to='symposion_schedule.Session', verbose_name='Session')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Session role',
                'verbose_name_plural': 'Session roles',
            },
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.TimeField(verbose_name='Start')),
                ('end', models.TimeField(verbose_name='End')),
                ('content_override', models.TextField(verbose_name='Content override', blank=True)),
                ('content_override_html', models.TextField(blank=True)),
                ('day', models.ForeignKey(to='symposion_schedule.Day', verbose_name='Day')),
            ],
            options={
                'ordering': ['day', 'start', 'end'],
                'verbose_name': 'slot',
                'verbose_name_plural': 'slots',
            },
        ),
        migrations.CreateModel(
            name='SlotKind',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50, verbose_name='Label')),
                ('schedule', models.ForeignKey(to='symposion_schedule.Schedule', verbose_name='schedule')),
            ],
            options={
                'verbose_name': 'Slot kind',
                'verbose_name_plural': 'Slot kinds',
            },
        ),
        migrations.CreateModel(
            name='SlotRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room', models.ForeignKey(to='symposion_schedule.Room', verbose_name='Room')),
                ('slot', models.ForeignKey(to='symposion_schedule.Slot', verbose_name='Slot')),
            ],
            options={
                'ordering': ['slot', 'room__order'],
                'verbose_name': 'Slot room',
                'verbose_name_plural': 'Slot rooms',
            },
        ),
        migrations.AddField(
            model_name='slot',
            name='kind',
            field=models.ForeignKey(to='symposion_schedule.SlotKind', verbose_name='Kind'),
        ),
        migrations.AddField(
            model_name='session',
            name='slots',
            field=models.ManyToManyField(related_name='sessions', verbose_name='Slots', to='symposion_schedule.Slot'),
        ),
        migrations.AddField(
            model_name='room',
            name='schedule',
            field=models.ForeignKey(to='symposion_schedule.Schedule', verbose_name='Schedule'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='slot',
            field=models.OneToOneField(to='symposion_schedule.Slot', related_name='content_ptr', blank=True, null=True, verbose_name='Slot'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='speaker',
            field=models.ForeignKey(to='symposion_speakers.Speaker', related_name='presentations', verbose_name='Speaker'),
        ),
        migrations.AddField(
            model_name='day',
            name='schedule',
            field=models.ForeignKey(to='symposion_schedule.Schedule', verbose_name='Schedule'),
        ),
        migrations.AlterUniqueTogether(
            name='slotroom',
            unique_together=set([('slot', 'room')]),
        ),
        migrations.AlterUniqueTogether(
            name='sessionrole',
            unique_together=set([('session', 'user', 'role')]),
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([('schedule', 'date')]),
        ),
    ]
