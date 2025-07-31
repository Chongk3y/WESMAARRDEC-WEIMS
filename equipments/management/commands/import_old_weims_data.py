import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from equipments.models import Equipment, Category, Status
from auth_user.models import User

class Command(BaseCommand):
    help = 'Import equipment data from old WEIMS database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--json-file',
            type=str,
            help='Path to JSON file containing exported data from old WEIMS'
        )
        parser.add_argument(
            '--sql-file', 
            type=str,
            help='Path to SQL dump file from old WEIMS database'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without actually importing'
        )

    def handle(self, *args, **options):
        if options['json_file']:
            self.import_from_json(options['json_file'], options['dry_run'])
        elif options['sql_file']:
            self.import_from_sql(options['sql_file'], options['dry_run'])
        else:
            self.stdout.write(
                self.style.ERROR('Please specify either --json-file or --sql-file option')
            )

    def import_from_json(self, json_file, dry_run=False):
        """Import data from JSON export"""
        if not os.path.exists(json_file):
            self.stdout.write(
                self.style.ERROR(f'JSON file not found: {json_file}')
            )
            return

        with open(json_file, 'r') as f:
            data = json.load(f)

        self.stdout.write(f"Found {len(data.get('equipments', []))} equipment records")
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No data will be imported'))
            return

        with transaction.atomic():
            # Import categories
            for cat_data in data.get('categories', []):
                category, created = Category.objects.get_or_create(
                    name=cat_data['name']
                )
                if created:
                    self.stdout.write(f"Created category: {category.name}")

            # Import statuses
            for status_data in data.get('statuses', []):
                status, created = Status.objects.get_or_create(
                    name=status_data['name']
                )
                if created:
                    self.stdout.write(f"Created status: {status.name}")

            # Import equipment
            for eq_data in data.get('equipments', []):
                self.import_equipment_record(eq_data)

        self.stdout.write(
            self.style.SUCCESS('Successfully imported all data!')
        )

    def import_equipment_record(self, eq_data):
        """Import a single equipment record"""
        try:
            # Get or create category
            category = None
            if eq_data.get('category'):
                category, _ = Category.objects.get_or_create(
                    name=eq_data['category']
                )

            # Get or create status
            status = None
            if eq_data.get('status'):
                status, _ = Status.objects.get_or_create(
                    name=eq_data['status']
                )

            # Get employee (emp field) - create a default user if needed
            emp = None
            if eq_data.get('emp_username'):
                try:
                    emp = User.objects.get(username=eq_data['emp_username'])
                except User.DoesNotExist:
                    # Create a placeholder user
                    emp = User.objects.create_user(
                        username=eq_data['emp_username'],
                        email=f"{eq_data['emp_username']}@wesmaarrdec.org",
                        password='changeme123'
                    )
                    self.stdout.write(f"Created user: {emp.username}")

            # Create equipment
            equipment = Equipment.objects.create(
                item_propertynum=eq_data.get('item_propertynum', ''),
                item_name=eq_data.get('item_name', ''),
                item_desc=eq_data.get('item_desc', ''),
                item_purdate=eq_data.get('item_purdate'),
                po_number=eq_data.get('po_number', ''),
                fund_source=eq_data.get('fund_source', ''),
                supplier=eq_data.get('supplier', ''),
                item_amount=eq_data.get('item_amount', 0),
                assigned_to=eq_data.get('assigned_to', ''),
                location=eq_data.get('location', ''),
                current_location=eq_data.get('current_location', ''),
                end_user=eq_data.get('end_user', ''),
                project_name=eq_data.get('project_name', ''),
                category=category,
                status=status,
                emp=emp,
                is_returned=eq_data.get('is_returned', False),
                is_archived=eq_data.get('is_archived', False),
                remarks=eq_data.get('remarks', ''),
            )
            
            self.stdout.write(f"Imported: {equipment.item_name}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing equipment {eq_data.get("item_name", "Unknown")}: {str(e)}')
            )

    def import_from_sql(self, sql_file, dry_run=False):
        """Handle SQL file import - provides instructions"""
        self.stdout.write(
            self.style.WARNING(
                'SQL file import requires manual steps. Here are the instructions:'
            )
        )
        self.stdout.write('\n1. First, backup your current database:')
        self.stdout.write('   mysqldump -u root -p wesmaarrdecdb > backup_current.sql')
        
        self.stdout.write('\n2. Extract equipment data from your old WEIMS database:')
        self.stdout.write('   mysqldump -u root -p old_weims_db equipments > old_equipments.sql')
        
        self.stdout.write('\n3. Modify the SQL file to match new table structure:')
        self.stdout.write('   - Update table names to match Django naming (equipments_equipment)')
        self.stdout.write('   - Update foreign key references')
        self.stdout.write('   - Handle user relationships')
        
        self.stdout.write('\n4. Import the modified SQL:')
        self.stdout.write('   mysql -u root -p wesmaarrdecdb < modified_equipments.sql')
        
        self.stdout.write(self.style.WARNING(
            '\nFor easier import, consider using the JSON export option instead.'
        ))
