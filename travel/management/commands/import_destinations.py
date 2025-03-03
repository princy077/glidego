import csv
from django.core.management.base import BaseCommand
from travel.models import Destination

class Command(BaseCommand):
    help = 'Import destinations from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = "travel/data/destinations.csv"  # Update path if needed

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Destination.objects.get_or_create(
                    name=row["name"],
                    description=row["description"],
                    location=row["location"],
                    category=row["category"],
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"])
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully imported destinations!'))
