"""
Management command to seed initial/default data for the WEIMS system.
This includes default categories and statuses for equipment.

Usage:
    python manage.py seed_initial_data
    python manage.py seed_initial_data --reset  # Removes and recreates
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from equipments.models import Category, Status


class Command(BaseCommand):
    help = 'Seeds initial data (categories and statuses) for the equipment management system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing categories and statuses before seeding',
        )

    def handle(self, *args, **options):
        reset = options.get('reset', False)
        
        with transaction.atomic():
            if reset:
                self.stdout.write(self.style.WARNING('Resetting existing data...'))
                Category.objects.all().delete()
                Status.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('✓ Existing data cleared'))
            
            # Seed Categories
            self.stdout.write('\nSeeding Categories...')
            categories = [
                'Appliances',
                'Audio Equipment',
                'Camera Equipment',
                'Computer Hardware',
                'Computer Peripheral',
                'Desktop Computer',
                'Display Equipments',
                'Furniture',
                'Laptop',
                'Mobile Devices',
                'Monitor',
                'Networking Device',
                'Office Equipment',
                'Other',
                'Printer',
                'Storage Devices',
                'UPS',
                'Vehicle',
            ]
            
            created_count = 0
            skipped_count = 0
            
            for category_name in categories:
                category, created = Category.objects.get_or_create(name=category_name)
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {category_name}'))
                else:
                    skipped_count += 1
                    self.stdout.write(f'  - Skipped (exists): {category_name}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Categories: {created_count} created, {skipped_count} already existed'
                )
            )
            
            # Seed Statuses
            self.stdout.write('\nSeeding Statuses...')
            statuses = [
                'Active',
                'Maintenance',
                'Damaged',
                'Lost',
                'Stored',
            ]
            
            created_count = 0
            skipped_count = 0
            
            for status_name in statuses:
                status, created = Status.objects.get_or_create(name=status_name)
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {status_name}'))
                else:
                    skipped_count += 1
                    self.stdout.write(f'  - Skipped (exists): {status_name}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Statuses: {created_count} created, {skipped_count} already existed'
                )
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n{"="*60}\n✓ Initial data seeding completed successfully!\n{"="*60}'
                )
            )
