"""
Test command for Word document generation
"""
from django.core.management.base import BaseCommand
from equipments.models import Equipment
from equipments.report_utils import generate_word_report_from_template
import os


class Command(BaseCommand):
    help = 'Test Word document generation with sample data'

    def handle(self, *args, **options):
        # Get some sample equipment data
        equipments = Equipment.objects.all()[:5]  # Get first 5 records for testing
        
        if not equipments:
            self.stdout.write(self.style.WARNING('No equipment records found. Please add some data first.'))
            return
        
        # Define test columns
        selected_columns = [
            'item_propertynum',
            'item_name', 
            'item_desc',
            'category',
            'status',
            'item_amount',
            'assigned_to',
            'location'
        ]
        
        # Column labels
        column_labels = {
            'item_propertynum': 'Property Number',
            'item_name': 'Equipment Name',
            'item_desc': 'Description', 
            'category': 'Category',
            'status': 'Status',
            'item_amount': 'Amount',
            'assigned_to': 'Assigned To',
            'location': 'Location'
        }
        
        try:
            # Generate Word document
            doc = generate_word_report_from_template(
                equipments=list(equipments),
                selected_columns=selected_columns,
                column_labels=column_labels
            )
            
            # Save to test file
            output_path = os.path.join('media', 'test_report.docx')
            doc.save(output_path)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully generated test Word document: {output_path}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error generating Word document: {str(e)}')
            )
