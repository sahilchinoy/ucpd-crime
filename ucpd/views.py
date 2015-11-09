import os
import csv
import json
from django.conf import settings
from django.db.models import Count, Max
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.core.serializers import serialize
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.http import Http404, HttpResponse
from bakery.views import BuildableTemplateView, BuildableDetailView
from ucpd.models import Incident, Bin, Statistics


class Main(BuildableTemplateView):
    """
    The landing page.
    """

    template_name = "main.html"
    build_path = "index.html"


# APIs
class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


class BuildableJSONView(JSONResponseMixin, BuildableTemplateView):
    # Nothing more than standard bakery configuration here
    build_path = 'jsonview.json'

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_content(self):
        """
        Overrides an internal trick of buildable views so that bakery
        can render the HttpResponse substituted above for the typical Django
        template by the JSONResponseMixin
        """
        return self.get(self.request).content


class BinsJSON(BuildableJSONView):
    """
    Returns GeoJSON of all bins with at least one incident.
    """

    build_path = "api/bins.json"

    def get_context_data(self, **kwargs):
        bins = Bin.objects.exclude(incidents=None)
        features = []
        for hbin in bins:
            as_dict = {
                "type": "Feature",
                "geometry": json.loads(hbin.geom.geojson),
                "properties": {
                    "id": hbin.id,
                }
            }
            features.append(as_dict)
        objects = {
            "type": "FeatureCollection",
            "features": features,
        }
        return objects


class BinDetailJSON(BuildableDetailView):
    """
    Returns counts and time-series data for a particular bin.
    """

    queryset = Bin.objects.exclude(incidents=None)

    def get_build_path(self, obj):
        dir_path = "api/bin"
        dir_path = os.path.join(settings.BUILD_DIR, dir_path)
        os.path.exists(dir_path) or os.makedirs(dir_path)
        path = os.path.join(dir_path,"{}.json".format(obj.id))
        return path

    def get_counts(self):
        """
        Returns count of incidents in this bin (excluding category N),
        broken across violent, property, and quality-of-life categories.
        Also returns maximum bin count.
        """
        counts = {}
        incidents = self.object.incidents.exclude(category='N')
        counts['total'] = incidents.count()
        counts['violent'] = incidents.filter(category='V').count()
        counts['property'] = incidents.filter(category='P').count()
        counts['QOL'] = incidents.filter(category='Q').count()

        stats = Statistics.objects.first()

        counts['max'] = {
            'total': stats.max_count,
            'violent': stats.max_V,
            'property': stats.max_P,
            'QOL': stats.max_Q
        }

        counts['mean'] = {
            'total': stats.mean_count,
            'violent': stats.mean_V,
            'property': stats.mean_P,
            'QOL': stats.mean_Q
        }

        counts['comparison'] = {}
        categories = ('total','violent','property','QOL')
        for category in categories:
            if counts[category] > counts['mean'][category]:
                counts['comparison'][category] = 'above'
            else:
                counts['comparison'][category] = 'below'

        counts['rank'] = self.object.rank
        counts['bin_count'] = stats.bin_count

        return counts

    def get_time_series(self):
        """
        Returns count of incidents in this bin (excluding category N),
        broken across violent, property, and quality-of-life categories.
        """

        stats = Statistics.objects.first()

        avg = {}
        avg['2010'] = stats.mean_10
        avg['2011'] = stats.mean_11
        avg['2012'] = stats.mean_12
        avg['2013'] = stats.mean_13
        avg['2014'] = stats.mean_14

        time_series = []
        time_comparison = {}

        for year in range(2010, 2015):
            incidents = self.object.incidents.exclude(category='N') \
                            .filter(date__year=year) 
            count = incidents.count()
            time_series.append({
                'Group': str(year),
                'count': count,
                'avg': avg[str(year)],
            })

        if time_series[3]['count'] > 0:
            diff = time_series[4]['count'] - time_series[3]['count']
            time_comparison = 100 * diff / time_series[3]['count']
        else:
            time_comparison = 100

        return time_series, time_comparison

    def get_context_data(self, **kwargs):
        context = {}
        context['counts'] = self.get_counts()
        context['time_series'], context['time_comparison'] = self.get_time_series()
        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_content(self):
        """
        Overrides an internal trick of buildable views so that bakery
        can render the HttpResponse substituted above for the typical Django
        template by the JSONResponseMixin
        """
        return self.get(self.request).content

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)

# Views to generate CSVs for visualizations

def hours(request):
    """
    Returns CSV of total crime, violent crime and property crime by hour
    by day.
    """
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="hours.csv"'

    writer = csv.writer(response)
    writer.writerow(['day', 'hour', 'total', 'violent', 'property'])
    for day in range(1,8):
        qset = Incident.objects.filter(date__week_day=day).exclude(category='N')
        for hour in range(0,24):
            count = qset.filter(time__hour=hour).count()
            v_count = qset.filter(time__hour=hour).filter(category='V').count()
            p_count = qset.filter(time__hour=hour).filter(category='P').count()
            writer.writerow([day, hour + 1, count, v_count, p_count])

    return response


def months(request):
    """
    Returns CSV of total crime, violent crime and property crime by month
    from 2010 to 2015.
    """
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="months.csv"'

    writer = csv.writer(response)
    writer.writerow(['date', 'Total', 'Violent', 'Property', 'Quality-of-life'])
    for year in range(2010, 2016):
        qset = Incident.objects.exclude(category='N').filter(date__year=year)
        for month in range(1,13):
            count = qset.filter(date__month=month).count()
            v_count = qset.filter(date__month=month).filter(category='V').count()
            p_count = qset.filter(date__month=month).filter(category='P').count()
            q_count = qset.filter(date__month=month).filter(category='Q').count()
            writer.writerow([str(month).zfill(2) + '/' + str(year), count, v_count, p_count, q_count])

    return response

