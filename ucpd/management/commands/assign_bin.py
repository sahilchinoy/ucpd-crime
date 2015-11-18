import logging
from django.db import transaction
from django.core.management.base import BaseCommand
from ucpd.models import Incident, Bin

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = "Assigns each incident a bin."

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Loops through incidents and, for each, finds the bin that intersects
        with the incident's geometry field, saving it to the incident's hbin
        field.
        """

        located = 0
        incidents = Incident.objects.exclude(point=None)
        logger.info(
            "Attempting to locate the {} of {} incidents with \
            a location".format(
                incidents.count(),
                Incident.objects.all().count()))

        for incident in incidents:
            bins = Bin.objects.filter(geom__contains=incident.point)
            if bins:
                incident.hbin = bins[0]
                incident.save()
                logger.info(
                    "Located incident {} at bin {}".format(
                        incident.caseno,
                        incident.hbin.id))
                located += 1
            else:
                logger.error(
                    "Did not assign bin to incident {}".format(
                        incident.caseno))

        logger.info(
            "Located {} of {} incidents".format(
                located,
                incidents.count()))
