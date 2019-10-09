# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import symposion.proposals.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('symposion_speakers', '__first__'),
        ('symposion_conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalSpeaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status', models.IntegerField(verbose_name='Status', default=1, choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Declined')])),
            ],
            options={
                'verbose_name': 'Addtional speaker',
                'verbose_name_plural': 'Additional speakers',
            },
        ),
        migrations.CreateModel(
            name='ProposalBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='Title', max_length=100)),
                ('description', models.TextField(verbose_name='Brief Description', max_length=400, help_text='If your proposal is accepted this will be made public and printed in the program. Should be one paragraph, maximum 400 characters.')),
                ('abstract', models.TextField(verbose_name='Detailed Abstract', help_text="Detailed outline. Will be made public if your proposal is accepted. Edit using <a href='http://daringfireball.net/projects/markdown/basics' target='_blank'>Markdown</a>.")),
                ('abstract_html', models.TextField(blank=True)),
                ('additional_notes', models.TextField(blank=True, verbose_name='Addtional Notes', help_text="Anything else you'd like the program committee to know when making their selection: your past experience, etc. This is not made public. Edit using <a href='http://daringfireball.net/projects/markdown/basics' target='_blank'>Markdown</a>.")),
                ('additional_notes_html', models.TextField(blank=True)),
                ('submitted', models.DateTimeField(editable=False, default=django.utils.timezone.now, verbose_name='Submitted')),
                ('cancelled', models.BooleanField(verbose_name='Cancelled', default=False)),
                ('additional_speakers', models.ManyToManyField(blank=True, verbose_name='Addtional speakers', through='symposion_proposals.AdditionalSpeaker', to='symposion_speakers.Speaker')),
            ],
        ),
        migrations.CreateModel(
            name='ProposalKind',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=100)),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('section', models.ForeignKey(to='symposion_conference.Section', verbose_name='Section', related_name='proposal_kinds')),
            ],
        ),
        migrations.CreateModel(
            name='ProposalSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('start', models.DateTimeField(blank=True, verbose_name='Start', null=True)),
                ('end', models.DateTimeField(blank=True, verbose_name='End', null=True)),
                ('closed', models.NullBooleanField(verbose_name='Closed')),
                ('published', models.NullBooleanField(verbose_name='Published')),
                ('section', models.OneToOneField(to='symposion_conference.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='SupportingDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(verbose_name='Created at', default=django.utils.timezone.now)),
                ('file', models.FileField(verbose_name='File', upload_to=symposion.proposals.models.uuid_filename)),
                ('description', models.CharField(verbose_name='Description', max_length=140)),
                ('proposal', models.ForeignKey(to='symposion_proposals.ProposalBase', verbose_name='Proposal', related_name='supporting_documents')),
                ('uploaded_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Uploaded by')),
            ],
        ),
        migrations.AddField(
            model_name='proposalbase',
            name='kind',
            field=models.ForeignKey(to='symposion_proposals.ProposalKind', verbose_name='Kind'),
        ),
        migrations.AddField(
            model_name='proposalbase',
            name='speaker',
            field=models.ForeignKey(to='symposion_speakers.Speaker', verbose_name='Speaker', related_name='proposals'),
        ),
        migrations.AddField(
            model_name='additionalspeaker',
            name='proposalbase',
            field=models.ForeignKey(to='symposion_proposals.ProposalBase', verbose_name='Proposalbase'),
        ),
        migrations.AddField(
            model_name='additionalspeaker',
            name='speaker',
            field=models.ForeignKey(to='symposion_speakers.Speaker', verbose_name='Speaker'),
        ),
        migrations.AlterUniqueTogether(
            name='additionalspeaker',
            unique_together=set([('speaker', 'proposalbase')]),
        ),
    ]
