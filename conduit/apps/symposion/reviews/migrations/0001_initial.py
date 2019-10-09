# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
from decimal import Decimal
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_proposals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.TextField(verbose_name='Text')),
                ('text_html', models.TextField(blank=True)),
                ('public', models.BooleanField(verbose_name='Public', default=False, choices=[(True, 'public'), (False, 'private')])),
                ('commented_at', models.DateTimeField(verbose_name='Commented at', default=datetime.datetime.now)),
                ('commenter', models.ForeignKey(verbose_name='Commenter', to=settings.AUTH_USER_MODEL)),
                ('proposal', models.ForeignKey(to='symposion_proposals.ProposalBase', verbose_name='Proposal', related_name='comments')),
            ],
            options={
                'verbose_name_plural': 'comments',
                'verbose_name': 'comment',
            },
        ),
        migrations.CreateModel(
            name='LatestVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('vote', models.CharField(choices=[('+1', '+1 \u2014 Good proposal and I will argue for it to be accepted.'), ('+0', '+0 \u2014 OK proposal, but I will not argue for it to be accepted.'), ('\u22120', '\u22120 \u2014 Weak proposal, but I will not argue strongly against acceptance.'), ('\u22121', '\u22121 \u2014 Serious issues and I will argue to reject this proposal.')], verbose_name='Vote', max_length=2)),
                ('submitted_at', models.DateTimeField(editable=False, verbose_name='Submitted at', default=datetime.datetime.now)),
                ('proposal', models.ForeignKey(to='symposion_proposals.ProposalBase', verbose_name='Proposal', related_name='votes')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'latest votes',
                'verbose_name': 'latest vote',
            },
        ),
        migrations.CreateModel(
            name='NotificationTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='Label', max_length=100)),
                ('from_address', models.EmailField(verbose_name='From address', max_length=254)),
                ('subject', models.CharField(verbose_name='Subject', max_length=100)),
                ('body', models.TextField(verbose_name='Body')),
            ],
            options={
                'verbose_name_plural': 'notification templates',
                'verbose_name': 'notification template',
            },
        ),
        migrations.CreateModel(
            name='ProposalMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('message', models.TextField(verbose_name='Message')),
                ('message_html', models.TextField(blank=True)),
                ('submitted_at', models.DateTimeField(editable=False, verbose_name='Submitted at', default=datetime.datetime.now)),
                ('proposal', models.ForeignKey(to='symposion_proposals.ProposalBase', verbose_name='Proposal', related_name='messages')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'proposal messages',
                'verbose_name': 'proposal message',
                'ordering': ['submitted_at'],
            },
        ),
        migrations.CreateModel(
            name='ProposalResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('score', models.DecimalField(decimal_places=2, verbose_name='Score', max_digits=5, default=Decimal('0.00'))),
                ('comment_count', models.PositiveIntegerField(verbose_name='Comment count', default=0)),
                ('vote_count', models.PositiveIntegerField(verbose_name='Vote count', default=0)),
                ('plus_one', models.PositiveIntegerField(verbose_name='Plus one', default=0)),
                ('plus_zero', models.PositiveIntegerField(verbose_name='Plus zero', default=0)),
                ('minus_zero', models.PositiveIntegerField(verbose_name='Minus zero', default=0)),
                ('minus_one', models.PositiveIntegerField(verbose_name='Minus one', default=0)),
                ('accepted', models.NullBooleanField(verbose_name='Accepted', default=None, choices=[(True, 'accepted'), (False, 'rejected'), (None, 'undecided')])),
                ('status', models.CharField(choices=[('accepted', 'accepted'), ('rejected', 'rejected'), ('undecided', 'undecided'), ('standby', 'standby')], verbose_name='Status', max_length=20, default='undecided')),
                ('proposal', models.OneToOneField(to='symposion_proposals.ProposalBase', verbose_name='Proposal', related_name='result')),
            ],
            options={
                'verbose_name_plural': 'proposal_results',
                'verbose_name': 'proposal_result',
            },
        ),
        migrations.CreateModel(
            name='ResultNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp', default=datetime.datetime.now)),
                ('to_address', models.EmailField(verbose_name='To address', max_length=254)),
                ('from_address', models.EmailField(verbose_name='From address', max_length=254)),
                ('subject', models.CharField(verbose_name='Subject', max_length=100)),
                ('body', models.TextField(verbose_name='Body')),
                ('proposal', models.ForeignKey(to='symposion_proposals.ProposalBase', verbose_name='Proposal', related_name='notifications')),
                ('template', models.ForeignKey(to='symposion_reviews.NotificationTemplate', blank=True, verbose_name='Template', null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('vote', models.CharField(blank=True, verbose_name='Vote', max_length=2, choices=[('+1', '+1 \u2014 Good proposal and I will argue for it to be accepted.'), ('+0', '+0 \u2014 OK proposal, but I will not argue for it to be accepted.'), ('\u22120', '\u22120 \u2014 Weak proposal, but I will not argue strongly against acceptance.'), ('\u22121', '\u22121 \u2014 Serious issues and I will argue to reject this proposal.')])),
                ('comment', models.TextField(verbose_name='Comment')),
                ('comment_html', models.TextField(blank=True)),
                ('submitted_at', models.DateTimeField(editable=False, verbose_name='Submitted at', default=datetime.datetime.now)),
                ('proposal', models.ForeignKey(to='symposion_proposals.ProposalBase', verbose_name='Proposal', related_name='reviews')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'reviews',
                'verbose_name': 'review',
            },
        ),
        migrations.CreateModel(
            name='ReviewAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('origin', models.IntegerField(choices=[(0, 'auto-assigned, initial'), (1, 'opted-in'), (2, 'auto-assigned, later')], verbose_name='Origin')),
                ('assigned_at', models.DateTimeField(verbose_name='Assigned at', default=datetime.datetime.now)),
                ('opted_out', models.BooleanField(verbose_name='Opted out', default=False)),
                ('proposal', models.ForeignKey(verbose_name='Proposal', to='symposion_proposals.ProposalBase')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='latestvote',
            unique_together=set([('proposal', 'user')]),
        ),
    ]
