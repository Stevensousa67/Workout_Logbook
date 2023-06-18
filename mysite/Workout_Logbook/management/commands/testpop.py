from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Used to debug and test multiple things'

    def handle(self, *args, **options):
        pass
