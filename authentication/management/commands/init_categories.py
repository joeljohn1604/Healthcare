import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_project.settings')
django.setup()

from django.core.management.base import BaseCommand
from authentication.models import Category

class Command(BaseCommand):
    help = 'Initialize blog categories'

    def handle(self, *args, **options):
        categories = [
            ('Mental Health', 'mental-health', 'Articles about mental health and wellbeing'),
            ('Heart Disease', 'heart-disease', 'Information about heart diseases and prevention'),
            ('Covid19', 'covid19', 'Latest updates and information about COVID-19'),
            ('Immunization', 'immunization', 'Vaccination and immunization information'),
        ]

        for name, slug, description in categories:
            Category.objects.get_or_create(
                name=name,
                defaults={'slug': slug, 'description': description}
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized categories'))