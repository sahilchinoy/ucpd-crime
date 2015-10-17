import logging
from django.core.management import call_command
from django.core.management.base import BaseCommand

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = "Set up the project by loading bins and \
    incidents, assigning classifications and bins, \
    and packing using tamper."

    def handle(self, *args, **options):
        call_command('load_bins')
        call_command('load_ucpd')
        call_command('classify')
        call_command('locate')
        call_command('assign_bin')
        call_command('pack')
