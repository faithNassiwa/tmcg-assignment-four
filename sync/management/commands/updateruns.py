from django.core.management import BaseCommand
from sync.models import Run


class Command(BaseCommand):
    def handle(self, *args, **options):
        added = Run.add_runs()
        self.stdout.write(self.style.SUCCESS('Successfully added %d runs' % added))
