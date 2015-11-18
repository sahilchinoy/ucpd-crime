import os
import csv
import logging
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from ucpd.models import Incident

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = "Load historical crime data from UCPD."

    def handle(self, *args, **options):
        Incident.objects.all().delete()

        dir_path = os.path.join(
            settings.DATA_DIR, 'ucpd')

        for path in [os.path.join(dir_path, file_path)
                     for file_path
                     in os.listdir(dir_path)
                     if file_path.endswith('.csv')]:

            # List of incidents we'll use in our bulk create
            bulk_incidents = []

            with open(path, 'rU') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    fields = {}

                    # If it doesn't have a case number, it's something like
                    # a security check, and we don't care about it
                    fields['caseno'] = row[2].strip()
                    if not fields['caseno']:
                        continue

                    fields['date'] = datetime.strptime(
                        row[0].strip(),
                        '%m/%d/%y')
                    fields['time'] = datetime.strptime(
                        row[1].strip(),
                        '%H:%M:%S')
                    fields['offense'] = row[3].strip()
                    fields['description'] = row[4].strip()
                    fields['address'] = row[5].strip()

                    bulk_incidents.append(Incident(**fields))
                    logger.info('Parsed case {}'.format(fields['caseno']))

            logger.info('Creating {} incidents'.format(len(bulk_incidents)))
            Incident.objects.bulk_create(bulk_incidents, batch_size=1000)
