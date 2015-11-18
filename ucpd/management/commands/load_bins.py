import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.utils import LayerMapping
from ucpd.models import Bin


class Command(BaseCommand):
    help = "Load shapefile of hexagonal bins into database."

    def handle(self, *args, **options):
        Bin.objects.all().delete()
        path = os.path.join(
            settings.DATA_DIR, 'bins', 'bins.shp')
        mapping = {"geom": "POLYGON"}
        lm = LayerMapping(
            Bin, path, mapping, source_srs=SpatialReference(3857))
        lm.save(verbose=True)
