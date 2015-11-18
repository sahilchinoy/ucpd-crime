import os
import json
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from Naked.toolshed.shell import execute_js
from ucpd.models import Incident


logger = logging.getLogger('django')


class Command(BaseCommand):
    help = "Packs incidents using tamper."

    def handle(self, *args, **options):
        # Write the incidents.json file to disk
        path_to_incidents = os.path.join(
            settings.BASE_DIR, 'pack', 'incidents.json')
        with open(path_to_incidents, 'w') as f:
            f.write(json.dumps(self.get_dict()))

        # Calls the node script that will pack the incidents
        # and store them in the static/json directory
        path_to_packer = os.path.join(
            settings.BASE_DIR, 'pack', 'pack.js')
        execute_js(path_to_packer)

        # Remove the incidents.json file
        os.remove(path_to_incidents)

    def get_dict(self):
        """
        Return dictionary of incidents used to serialize into json.
        """
        features = []
        incidents = Incident.objects.exclude(hbin=None).exclude(category='N')
        for incident in incidents:
            features.append(incident.as_dict())
        return {"incidents": features}
