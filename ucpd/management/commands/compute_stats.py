import os
import csv
import logging
import numpy as np
from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand
from ucpd.models import Bin, Statistics

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = "Compute statistics."

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Loop through bins, computing maximum, minimum
        and averages for all incident types, violent incidents
        only, property incidents only and quality-of-life
        incidents only.
        """

        counts = []
        V_counts = []
        P_counts = []
        Q_counts = []
        counts_10 = []
        counts_11 = []
        counts_12 = []
        counts_13 = []
        counts_14 = []

        for hbin in Bin.objects.exclude(incidents=None):
            incidents = hbin.incidents.exclude(category='N')
            counts.append(incidents.count())

            V_incidents = incidents.filter(category='V')
            V_counts.append(V_incidents.count())

            P_incidents = incidents.filter(category='P')
            P_counts.append(P_incidents.count())

            Q_incidents = incidents.filter(category='Q')
            Q_counts.append(Q_incidents.count())

            incidents_10 = incidents.filter(date__year=2010)
            counts_10.append(incidents_10.count())

            incidents_11 = incidents.filter(date__year=2011)
            counts_11.append(incidents_11.count())

            incidents_12 = incidents.filter(date__year=2012)
            counts_12.append(incidents_12.count())

            incidents_13 = incidents.filter(date__year=2013)
            counts_13.append(incidents_13.count())

            incidents_14 = incidents.filter(date__year=2014)
            counts_14.append(incidents_14.count())

        Statistics.objects.all().delete()
        Statistics(
            max_count = np.max(counts),
            max_V = np.max(V_counts),
            max_P = np.max(P_counts),
            max_Q = np.max(Q_counts),

            min_count = np.min(counts),
            min_V = np.min(V_counts),
            min_P = np.min(P_counts),
            min_Q = np.min(Q_counts),

            mean_count = np.mean(counts),
            mean_V = np.mean(V_counts),
            mean_P = np.mean(P_counts),
            mean_Q = np.mean(Q_counts),

            mean_10 = np.mean(counts_10),
            mean_11 = np.mean(counts_11),
            mean_12 = np.mean(counts_12),
            mean_13 = np.mean(counts_13),
            mean_14 = np.mean(counts_14)
        ).save()

        logger.info('Computed statistics.')
