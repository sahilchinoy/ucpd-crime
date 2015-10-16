import json
from django.contrib.gis.db import models


class Bin(models.Model):
    """
    Hexagonal bins, created using QGIS and imported using the load_bins command.
    """

    geom = models.PolygonField(srid=4326, null=True)
    population = models.FloatField(null=True)

    objects = models.GeoManager()

    def get_absolute_url(self):
        return "/bins/{}/".format(self.id)

class Incident(models.Model):
    """
    A single criminal incident reported to UCPD.
    """

    # Provided in raw data
    caseno = models.CharField(
        db_index=True,
        max_length=10,
        help_text='Case number')
    address = models.CharField(max_length=200, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    offense = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    # Assigned category code
    CATEGORY_CHOICES = (
        ('V', 'Violent'),
        ('P', 'Property'),
        ('Q', 'Quality of life'),
        ('N', 'Uncategorized'),
    )
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        default='N'
    )

    # Geographic information
    point = models.PointField(null=True)

    # Associate with bin
    hbin = models.ForeignKey(
        Bin,
        null=True,
        related_name='incidents'
    )

    objects = models.GeoManager()

    class Meta:
        ordering = ['-caseno']

    def __unicode__(self):
        return "Incident {}: {}".format(self.caseno, self.offense)

    def as_dict(self):
        """
        Method to return an incident as a dictionary.
        """

        as_dict = {
            "bin": str(self.hbin.id),
            "year": str(self.date.year),
            "month": str(self.date.month),
            "month_year": str(self.date.month) + ' ' + str(self.date.year),
            "day": str(self.date.day),
            "hour": str(self.time.hour),
            "category": self.category
        }
        return as_dict
