import os
import csv
import logging
from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand
from ucpd.models import Incident

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = "Assign each incident in the database a classification."

    def build_classifier(self):
        """
        Use CSV mapping to build dictionary of incident descriptions
        to canonical descriptions and categories.
        """

        classifier = {}
        path = os.path.join(settings.DATA_DIR,'classification.csv')
        with open(path,'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                classifier[row['key']] = (row['description'], row['category'])
        return classifier


    @transaction.atomic
    def handle(self, *args, **options):
        """
        Loop through incidents, using classifier dictionary to assign
        each incident a category and description.
        """

        classifier = self.build_classifier()

        for incident in Incident.objects.all():
            try:
                _type, category = classifier[incident.offense]
            except KeyError:
                logger.error('Error on Incident {} of offense type {}'.format(
                    incident.caseno,
                    incident.offense))
                continue

            incident.category = category
            incident.save()

            logger.info(
                "Assigned Incident {} category {}".format(
                    incident.caseno,
                    incident.category))
