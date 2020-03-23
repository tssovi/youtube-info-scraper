from django.core.management.base import BaseCommand
from common.auto_updater import StartAutoUpdater


class Command(BaseCommand):
    help = 'Auto Data Updater Is Running'

    def handle(self, *args, **kwargs):
        StartAutoUpdater()


