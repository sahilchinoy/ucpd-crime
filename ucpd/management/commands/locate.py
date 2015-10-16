import os
import csv
import logging
from django.conf import settings
from django.contrib.gis.geos import fromstr
from django.core.management.base import BaseCommand
from ucpd.models import Incident

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = "Geocode each incident."

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Loop through incidents, using a .csv file of addresses to lat/long
        pairs to geocode each incident.
        """

        # Build a dictionary of addresses that we've checked for accuracy
        addresses = {}
        addresses_path = os.path.join(
            settings.DATA_DIR,
            'ucpd',
            'addresses.csv'
        )
        with open(addresses_path, 'r') as addresses_file:
            reader = csv.DictReader(addresses_file)
            for row in reader:
                if row['checked']:
                    addresses[row['db_name']] = {
                        'canonical_name': row['canonical_name'],
                        'lat': row['lat'],
                        'lon': row['long']
                    }
        logger.info('Built dictionary of {} addresses'.format(len(addresses)))

        counter = 0
        for incident in Incident.objects.all():
            geocoded_dict = addresses.get(incident.address)
            if geocoded_dict and geocoded_dict['lat']:
                _str = 'POINT(' + geocoded_dict['lon'] + ' ' + geocoded_dict['lat'] + ')'
                incident.point = fromstr(_str, srid=4326)
                incident.save()
                counter += 1
                logger.info('Geocoded {}'.format(incident.address))

        logger.info('Geocoded {} incidents'.format(counter))
