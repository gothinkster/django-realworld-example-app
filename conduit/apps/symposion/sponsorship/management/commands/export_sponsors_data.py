import csv
import os
import shutil
import zipfile

from contextlib import closing

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from sotmjp.sponsorship.models import Sponsor


def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(zipfile.ZipFile(archivename, "w", zipfile.ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir) + len(os.sep):]     # XXX: relative path
                z.write(absfn, zfn)


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            os.makedirs(os.path.join(os.getcwd(), "build"))
        except:
            pass

        csv_file = csv.writer(
            open(os.path.join(os.getcwd(), "build", "sponsors.csv"), "wb")
        )
        csv_file.writerow(["Name", "URL", "Level", "Description"])

        for sponsor in Sponsor.objects.all():
            path = os.path.join(os.getcwd(), "build", slugify(sponsor.name))
            try:
                os.makedirs(path)
            except:
                pass

            data = {
                "name": sponsor.name,
                "url": sponsor.external_url,
                "level": sponsor.level.name,
                "description": "",
            }
            for sponsor_benefit in sponsor.sponsor_benefits.all():
                if sponsor_benefit.benefit_id == 2:
                    data["description"] = sponsor_benefit.text
                if sponsor_benefit.benefit_id == 1:
                    if sponsor_benefit.upload:
                        data["ad"] = sponsor_benefit.upload.path
                if sponsor_benefit.benefit_id == 7:
                    if sponsor_benefit.upload:
                        data["logo"] = sponsor_benefit.upload.path

            if "ad" in data:
                ad_path = data.pop("ad")
                shutil.copy(ad_path, path)
            if "logo" in data:
                logo_path = data.pop("logo")
                shutil.copy(logo_path, path)

            csv_file.writerow([
                data["name"].encode("utf-8"),
                data["url"].encode("utf-8"),
                data["level"].encode("utf-8"),
                data["description"].encode("utf-8")
            ])

        zipdir(
            os.path.join(os.getcwd(), "build"),
            os.path.join(os.getcwd(), "sponsors.zip"))
