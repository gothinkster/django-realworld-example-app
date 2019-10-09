# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('symposion_conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=100)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('type', models.CharField(default='simple', choices=[('text', 'Text'), ('file', 'File'), ('richtext', 'Rich Text'), ('weblogo', 'Web Logo'), ('simple', 'Simple'), ('option', 'Option')], verbose_name='Type', max_length=10)),
                ('content_type', models.CharField(default='simple', choices=[('simple', 'Simple'), ('listing_text_af', 'Listing Text (Afrikaans)'), ('listing_text_ar', 'Listing Text (Arabic)'), ('listing_text_ast', 'Listing Text (Asturian)'), ('listing_text_az', 'Listing Text (Azerbaijani)'), ('listing_text_bg', 'Listing Text (Bulgarian)'), ('listing_text_be', 'Listing Text (Belarusian)'), ('listing_text_bn', 'Listing Text (Bengali)'), ('listing_text_br', 'Listing Text (Breton)'), ('listing_text_bs', 'Listing Text (Bosnian)'), ('listing_text_ca', 'Listing Text (Catalan)'), ('listing_text_cs', 'Listing Text (Czech)'), ('listing_text_cy', 'Listing Text (Welsh)'), ('listing_text_da', 'Listing Text (Danish)'), ('listing_text_de', 'Listing Text (German)'), ('listing_text_el', 'Listing Text (Greek)'), ('listing_text_en', 'Listing Text (English)'), ('listing_text_en-au', 'Listing Text (Australian English)'), ('listing_text_en-gb', 'Listing Text (British English)'), ('listing_text_eo', 'Listing Text (Esperanto)'), ('listing_text_es', 'Listing Text (Spanish)'), ('listing_text_es-ar', 'Listing Text (Argentinian Spanish)'), ('listing_text_es-mx', 'Listing Text (Mexican Spanish)'), ('listing_text_es-ni', 'Listing Text (Nicaraguan Spanish)'), ('listing_text_es-ve', 'Listing Text (Venezuelan Spanish)'), ('listing_text_et', 'Listing Text (Estonian)'), ('listing_text_eu', 'Listing Text (Basque)'), ('listing_text_fa', 'Listing Text (Persian)'), ('listing_text_fi', 'Listing Text (Finnish)'), ('listing_text_fr', 'Listing Text (French)'), ('listing_text_fy', 'Listing Text (Frisian)'), ('listing_text_ga', 'Listing Text (Irish)'), ('listing_text_gl', 'Listing Text (Galician)'), ('listing_text_he', 'Listing Text (Hebrew)'), ('listing_text_hi', 'Listing Text (Hindi)'), ('listing_text_hr', 'Listing Text (Croatian)'), ('listing_text_hu', 'Listing Text (Hungarian)'), ('listing_text_ia', 'Listing Text (Interlingua)'), ('listing_text_id', 'Listing Text (Indonesian)'), ('listing_text_io', 'Listing Text (Ido)'), ('listing_text_is', 'Listing Text (Icelandic)'), ('listing_text_it', 'Listing Text (Italian)'), ('listing_text_ja', 'Listing Text (Japanese)'), ('listing_text_ka', 'Listing Text (Georgian)'), ('listing_text_kk', 'Listing Text (Kazakh)'), ('listing_text_km', 'Listing Text (Khmer)'), ('listing_text_kn', 'Listing Text (Kannada)'), ('listing_text_ko', 'Listing Text (Korean)'), ('listing_text_lb', 'Listing Text (Luxembourgish)'), ('listing_text_lt', 'Listing Text (Lithuanian)'), ('listing_text_lv', 'Listing Text (Latvian)'), ('listing_text_mk', 'Listing Text (Macedonian)'), ('listing_text_ml', 'Listing Text (Malayalam)'), ('listing_text_mn', 'Listing Text (Mongolian)'), ('listing_text_mr', 'Listing Text (Marathi)'), ('listing_text_my', 'Listing Text (Burmese)'), ('listing_text_nb', 'Listing Text (Norwegian Bokmal)'), ('listing_text_ne', 'Listing Text (Nepali)'), ('listing_text_nl', 'Listing Text (Dutch)'), ('listing_text_nn', 'Listing Text (Norwegian Nynorsk)'), ('listing_text_os', 'Listing Text (Ossetic)'), ('listing_text_pa', 'Listing Text (Punjabi)'), ('listing_text_pl', 'Listing Text (Polish)'), ('listing_text_pt', 'Listing Text (Portuguese)'), ('listing_text_pt-br', 'Listing Text (Brazilian Portuguese)'), ('listing_text_ro', 'Listing Text (Romanian)'), ('listing_text_ru', 'Listing Text (Russian)'), ('listing_text_sk', 'Listing Text (Slovak)'), ('listing_text_sl', 'Listing Text (Slovenian)'), ('listing_text_sq', 'Listing Text (Albanian)'), ('listing_text_sr', 'Listing Text (Serbian)'), ('listing_text_sr-latn', 'Listing Text (Serbian Latin)'), ('listing_text_sv', 'Listing Text (Swedish)'), ('listing_text_sw', 'Listing Text (Swahili)'), ('listing_text_ta', 'Listing Text (Tamil)'), ('listing_text_te', 'Listing Text (Telugu)'), ('listing_text_th', 'Listing Text (Thai)'), ('listing_text_tr', 'Listing Text (Turkish)'), ('listing_text_tt', 'Listing Text (Tatar)'), ('listing_text_udm', 'Listing Text (Udmurt)'), ('listing_text_uk', 'Listing Text (Ukrainian)'), ('listing_text_ur', 'Listing Text (Urdu)'), ('listing_text_vi', 'Listing Text (Vietnamese)'), ('listing_text_zh-cn', 'Listing Text (Simplified Chinese)'), ('listing_text_zh-hans', 'Listing Text (Simplified Chinese)'), ('listing_text_zh-hant', 'Listing Text (Traditional Chinese)'), ('listing_text_zh-tw', 'Listing Text (Traditional Chinese)')], verbose_name='content type', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='BenefitLevel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('max_words', models.PositiveIntegerField(blank=True, verbose_name='Max words', null=True)),
                ('other_limits', models.CharField(blank=True, verbose_name='Other limits', max_length=200)),
                ('benefit', models.ForeignKey(to='symposion_sponsorship.Benefit', related_name='benefit_levels', verbose_name='Benefit')),
            ],
            options={
                'verbose_name_plural': 'Benefit levels',
                'ordering': ['level'],
                'verbose_name': 'Benefit level',
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Sponsor Name', max_length=100)),
                ('display_url', models.URLField(blank=True, verbose_name='display URL')),
                ('external_url', models.URLField(verbose_name='External URL')),
                ('annotation', models.TextField(blank=True, verbose_name='Annotation')),
                ('contact_name', models.CharField(verbose_name='Contact Name', max_length=100)),
                ('contact_email', models.EmailField(verbose_name='Contact Email', max_length=254)),
                ('added', models.DateTimeField(default=datetime.datetime.now, verbose_name='added')),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('web_logo_benefit', models.NullBooleanField(verbose_name='Web logo benefit', help_text='Web logo benefit is complete')),
                ('print_logo_benefit', models.NullBooleanField(verbose_name='Print logo benefit', help_text='Print logo benefit is complete')),
                ('print_description_benefit', models.NullBooleanField(verbose_name='Print description benefit', help_text='Print description benefit is complete')),
                ('company_description_benefit', models.NullBooleanField(verbose_name='Company description benefit', help_text='Company description benefit is complete')),
                ('applicant', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='sponsorships', verbose_name='Applicant')),
            ],
            options={
                'verbose_name_plural': 'Sponsors',
                'ordering': ['name'],
                'verbose_name': 'Sponsor',
            },
        ),
        migrations.CreateModel(
            name='SponsorBenefit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('max_words', models.PositiveIntegerField(blank=True, verbose_name='Max words', null=True)),
                ('other_limits', models.CharField(blank=True, verbose_name='Other limits', max_length=200)),
                ('text', models.TextField(blank=True, verbose_name='Text')),
                ('upload', models.FileField(blank=True, verbose_name='File', upload_to='sponsor_files')),
                ('is_complete', models.NullBooleanField(verbose_name='Complete?', help_text='True - benefit complete; False - benefit incomplete; Null - n/a')),
                ('benefit', models.ForeignKey(to='symposion_sponsorship.Benefit', related_name='sponsor_benefits', verbose_name='Benefit')),
                ('sponsor', models.ForeignKey(to='symposion_sponsorship.Sponsor', related_name='sponsor_benefits', verbose_name='Sponsor')),
            ],
            options={
                'verbose_name_plural': 'Sponsor benefits',
                'ordering': ['-active'],
                'verbose_name': 'Sponsor benefit',
            },
        ),
        migrations.CreateModel(
            name='SponsorLevel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=100)),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('cost', models.PositiveIntegerField(verbose_name='Cost')),
                ('description', models.TextField(blank=True, verbose_name='Description', help_text='This is private.')),
                ('conference', models.ForeignKey(to='symposion_conference.Conference', verbose_name='Conference')),
            ],
            options={
                'verbose_name_plural': 'Sponsor levels',
                'ordering': ['conference', 'order'],
                'verbose_name': 'Sponsor level',
            },
        ),
        migrations.AddField(
            model_name='sponsor',
            name='level',
            field=models.ForeignKey(to='symposion_sponsorship.SponsorLevel', verbose_name='level'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='sponsor_logo',
            field=models.ForeignKey(blank=True, to='symposion_sponsorship.SponsorBenefit', null=True, related_name='+', verbose_name='Sponsor logo', editable=False),
        ),
        migrations.AddField(
            model_name='benefitlevel',
            name='level',
            field=models.ForeignKey(to='symposion_sponsorship.SponsorLevel', related_name='benefit_levels', verbose_name='Level'),
        ),
    ]
