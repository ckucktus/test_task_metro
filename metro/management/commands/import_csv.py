from django.core.management.base import BaseCommand, CommandError
from metro.models import Metro
import csv
import os
from dotenv import load_dotenv

load_dotenv()

def import_csv_to_db():
    with open(os.getenv('CSV')) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] not in ['Station', 'station']:
                _, created = Metro.objects.get_or_create(
                    station=row[0],
                    line=row[1],
                    admarea=row[2],
                    district=row[3],
                    status=row[4],
                    ID=row[5]
                    )

class Command(BaseCommand):
    help = 'importscv'

    def handle(self, *args, **kwargs):
        try:
           import_csv_to_db()
        except:
            raise CommandError('Initalization failed.')
