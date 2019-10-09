from cStringIO import StringIO
import os
import shutil
import tempfile
from zipfile import ZipFile

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from pycon.sponsorship.models import Benefit, Sponsor, SponsorBenefit,\
    SponsorLevel
from symposion.conference.models import current_conference


class TestSponsorZipDownload(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='joe',
                                             email='joe@example.com',
                                             password='joe')
        self.user.is_staff = True
        self.user.save()
        self.url = reverse("sponsor_zip_logos")
        self.assertTrue(self.client.login(username='joe@example.com',
                                          password='joe'))

        # we need a sponsor
        conference = current_conference()
        self.sponsor_level = SponsorLevel.objects.create(
            conference=conference, name="Lead", cost=1)
        self.sponsor = Sponsor.objects.create(
            name="Big Daddy",
            level=self.sponsor_level,
            active=True,
        )

        # Create our benefits, of various types
        self.text_benefit = Benefit.objects.create(name="text", type="text")
        self.file_benefit = Benefit.objects.create(name="file", type="file")
        # These names must be spelled exactly this way:
        self.weblogo_benefit = Benefit.objects.create(name="Web logo", type="weblogo")
        self.printlogo_benefit = Benefit.objects.create(name="Print logo", type="file")
        self.advertisement_benefit = Benefit.objects.create(name="Advertisement", type="file")

    def validate_response(self, rsp, names_and_sizes):
        # Ensure a response from the view looks right, contains a valid
        # zip archive, has files with the right names and sizes.
        self.assertEqual("application/zip", rsp['Content-type'])
        prefix = settings.CONFERENCE_URL_PREFIXES[settings.CONFERENCE_ID]

        self.assertEqual(
            'attachment; filename="pycon_%s_sponsorlogos.zip"' % prefix,
            rsp['Content-Disposition'])
        zipfile = ZipFile(StringIO(rsp.content), "r")
        # Check out the zip - testzip() returns None if no errors found
        self.assertIsNone(zipfile.testzip())
        # Compare contents to what is expected
        infolist = zipfile.infolist()
        self.assertEqual(len(names_and_sizes), len(infolist))
        for info, name_and_size in zip(infolist, names_and_sizes):
            name, size = name_and_size
            self.assertEqual(name, info.filename)
            self.assertEqual(size, info.file_size)

    def make_temp_file(self, name, size=0):
        # Create a temp file with the given name and size under self.temp_dir
        path = os.path.join(self.temp_dir, name)
        with open(path, "wb") as f:
            f.write(size * "x")

    def test_must_be_logged_in(self):
        # Must be logged in to use the view
        # If not logged in, doesn't redirect, just serves up a login view
        self.client.logout()
        rsp = self.client.get(self.url)
        self.assertEqual(200, rsp.status_code)
        self.assertIn("""<body class="login">""", rsp.content)

    def test_must_be_staff(self):
        # Only staff can use the view
        # If not staff, doesn't show error, just serves up a login view
        # Also, the dashboard doesn't show the download button
        self.user.is_staff = False
        self.user.save()
        rsp = self.client.get(self.url)
        self.assertEqual(200, rsp.status_code)
        self.assertIn("""<body class="login">""", rsp.content)
        rsp = self.client.get(reverse('dashboard'))
        self.assertNotIn(self.url, rsp.content)

    def test_no_files(self):
        # If there are no sponsor files, we still work
        # And the dashboard shows our download button
        rsp = self.client.get(self.url)
        self.validate_response(rsp, [])
        rsp = self.client.get(reverse('dashboard'))
        self.assertIn(self.url, rsp.content)

    def test_different_benefit_types(self):
        # We only get files from the benefits named "Print logo" and "Web logo"
        # And we ignore any non-existent files
        try:
            # Create a temp dir for media files
            self.temp_dir = tempfile.mkdtemp()
            with override_settings(MEDIA_ROOT=self.temp_dir):

                # Give our sponsor some benefits
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.text_benefit,
                    text="Foo!"
                )

                self.make_temp_file("file1", 10)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.file_benefit,
                    upload="file1"
                )

                self.make_temp_file("file2", 20)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.weblogo_benefit,
                    upload="file2"
                )

                # Benefit whose file is missing from the disk
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.weblogo_benefit,
                    upload="file3"
                )

                # print logo benefit
                self.make_temp_file("file4", 40)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.printlogo_benefit,
                    upload="file4"
                )

                self.make_temp_file("file5", 50)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.advertisement_benefit,
                    upload="file5"
                )

                rsp = self.client.get(self.url)
                expected = [
                    ('web_logos/lead/big_daddy/file2', 20),
                    ('print_logos/lead/big_daddy/file4', 40),
                    ('advertisement/lead/big_daddy/file5', 50)
                ]
                self.validate_response(rsp, expected)
        finally:
            if hasattr(self, 'temp_dir'):
                # Clean up any temp media files
                shutil.rmtree(self.temp_dir)

    def test_file_org(self):
        # The zip file is organized into directories:
        #  {print_logos,web_logos,advertisement}/<sponsor_level>/<sponsor_name>/<filename>

        # Add another sponsor at a different sponsor level
        conference = current_conference()
        self.sponsor_level2 = SponsorLevel.objects.create(
            conference=conference, name="Silly putty", cost=1)
        self.sponsor2 = Sponsor.objects.create(
            name="Big Mama",
            level=self.sponsor_level2,
            active=True,
        )
        #
        try:
            # Create a temp dir for media files
            self.temp_dir = tempfile.mkdtemp()
            with override_settings(MEDIA_ROOT=self.temp_dir):

                # Give our sponsors some benefits
                self.make_temp_file("file1", 10)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.weblogo_benefit,
                    upload="file1"
                )
                # print logo benefit
                self.make_temp_file("file2", 20)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor,
                    benefit=self.printlogo_benefit,
                    upload="file2"
                )
                # Sponsor 2
                self.make_temp_file("file3", 30)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor2,
                    benefit=self.weblogo_benefit,
                    upload="file3"
                )
                # print logo benefit
                self.make_temp_file("file4", 42)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor2,
                    benefit=self.printlogo_benefit,
                    upload="file4"
                )
                # ad benefit
                self.make_temp_file("file5", 55)
                SponsorBenefit.objects.create(
                    sponsor=self.sponsor2,
                    benefit=self.advertisement_benefit,
                    upload="file5"
                )

                rsp = self.client.get(self.url)
                expected = [
                    ('web_logos/lead/big_daddy/file1', 10),
                    ('web_logos/silly_putty/big_mama/file3', 30),
                    ('print_logos/lead/big_daddy/file2', 20),
                    ('print_logos/silly_putty/big_mama/file4', 42),
                    ('advertisement/silly_putty/big_mama/file5', 55),
                ]
                self.validate_response(rsp, expected)
        finally:
            if hasattr(self, 'temp_dir'):
                # Clean up any temp media files
                shutil.rmtree(self.temp_dir)


class TestBenefitValidation(TestCase):
    """
    It should not be possible to save a SponsorBenefit if it has the
    wrong kind of data in it - e.g. a text-type benefit cannot have
    an uploaded file, and vice-versa.
    """
    def setUp(self):
        # we need a sponsor
        conference = current_conference()
        self.sponsor_level = SponsorLevel.objects.create(
            conference=conference, name="Lead", cost=1)
        self.sponsor = Sponsor.objects.create(
            name="Big Daddy",
            level=self.sponsor_level,
        )

        # Create our benefit types
        self.text_type = Benefit.objects.create(name="text", type="text")
        self.file_type = Benefit.objects.create(name="file", type="file")
        self.weblogo_type = Benefit.objects.create(name="log", type="weblogo")
        self.simple_type = Benefit.objects.create(name="simple", type="simple")

    def validate(self, should_work, benefit_type, upload, text):
        obj = SponsorBenefit(
            benefit=benefit_type,
            sponsor=self.sponsor,
            upload=upload,
            text=text
        )
        if should_work:
            obj.save()
        else:
            with self.assertRaises(ValidationError):
                obj.save()

    def test_text_has_text(self):
        self.validate(True, self.text_type, upload=None, text="Some text")

    def test_text_has_upload(self):
        self.validate(False, self.text_type, upload="filename", text='')

    def test_text_has_both(self):
        self.validate(False, self.text_type, upload="filename", text="Text")

    def test_file_has_text(self):
        self.validate(False, self.file_type, upload=None, text="Some text")

    def test_file_has_upload(self):
        self.validate(True, self.file_type, upload="filename", text='')

    def test_file_has_both(self):
        self.validate(False, self.file_type, upload="filename", text="Text")

    def test_weblogo_has_text(self):
        self.validate(False, self.weblogo_type, upload=None, text="Some text")

    def test_weblogo_has_upload(self):
        self.validate(True, self.weblogo_type, upload="filename", text='')

    def test_weblogo_has_both(self):
        self.validate(False, self.weblogo_type, upload="filename", text="Text")

    def test_simple_has_neither(self):
        self.validate(True, self.simple_type, upload=None, text='')

    def test_simple_has_text(self):
        self.validate(True, self.simple_type, upload=None, text="Some text")

    def test_simple_has_upload(self):
        self.validate(False, self.simple_type, upload="filename", text='')

    def test_simple_has_both(self):
        self.validate(False, self.simple_type, upload="filename", text="Text")
