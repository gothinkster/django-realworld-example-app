import csv
import os

from django.core.management.base import BaseCommand

from symposion.speakers.models import Speaker


class Command(BaseCommand):

    def handle(self, *args, **options):
        csv_file = csv.writer(open(os.path.join(os.getcwd(), "speakers.csv"), "wb"))
        csv_file.writerow(["Name", "Bio"])

        for speaker in Speaker.objects.all():
            csv_file.writerow([
                speaker.name.encode("utf-8"),
                speaker.biography.encode("utf-8"),
            ])
