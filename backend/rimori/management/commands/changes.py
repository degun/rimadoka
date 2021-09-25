from django.core.management.base import BaseCommand
from rimori.models import Word

class Command(BaseCommand):
    help = 'Make changes to the database'

    def handle(self, *args, **options):
        cwords = Word.objects.all().count()
        print(cwords)