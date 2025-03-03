import csv
from django.core.management.base import BaseCommand
from travel.models import Activity, Destination

class Command(BaseCommand):
    help = 'Import activities from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = "travel/data/activities.csv"  # Ensure this file exists

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                destination = Destination.objects.filter(name=row["destination_name"]).first()

                if destination:
                    Activity.objects.get_or_create(
                        name=row["activity_name"],
                        activity_type=row["activity_type"],
                        destination=destination,
                        price=float(row["price"])
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully imported activities!'))
