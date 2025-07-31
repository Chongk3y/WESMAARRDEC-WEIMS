from django.core.management.base import BaseCommand
from django.db import connection
from equipments.models import Equipment, Category, Status

class Command(BaseCommand):
    help = 'Show current WEIMS database structure for data mapping'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== CURRENT WEIMS DATABASE STRUCTURE ==='))
        
        # Show Django table names and structure
        self.show_table_structure('equipments_category', 'CATEGORY')
        self.show_table_structure('equipments_status', 'STATUS')  
        self.show_table_structure('equipments_equipment', 'EQUIPMENT')
        self.show_table_structure('auth_user_user', 'USER (for emp field)')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('FIELD MAPPING GUIDE:')
        self.stdout.write('='*50)
        
        self.show_field_mapping()

    def show_table_structure(self, table_name, label):
        self.stdout.write(f'\n{label} TABLE ({table_name}):')
        self.stdout.write('-' * 40)
        
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"DESCRIBE {table_name};")
                rows = cursor.fetchall()
                
                for row in rows:
                    field, field_type, null, key, default, extra = row
                    nullable = "NULL" if null == "YES" else "NOT NULL"
                    key_info = f" [{key}]" if key else ""
                    default_info = f" DEFAULT({default})" if default else ""
                    
                    self.stdout.write(f"  {field:<20} {field_type:<15} {nullable}{key_info}{default_info}")
            
            except Exception as e:
                self.stdout.write(f"  Error describing table: {e}")

    def show_field_mapping(self):
        """Show how to map old WEIMS fields to new Django fields"""
        
        mappings = {
            'EQUIPMENT': {
                'old_field_examples': {
                    'id': 'id (AUTO_INCREMENT)',
                    'property_number': 'item_propertynum',
                    'name/title': 'item_name', 
                    'description': 'item_desc',
                    'purchase_date': 'item_purdate',
                    'po_number': 'po_number',
                    'amount/cost': 'item_amount',
                    'category_id': 'category_id (FK to equipments_category)',
                    'status_id': 'status_id (FK to equipments_status)',
                    'employee_id': 'emp_id (FK to auth_user_user)',
                    'end_user': 'end_user',
                    'location': 'location',
                    'current_location': 'current_location',
                    'assigned_to': 'assigned_to',
                    'fund_source': 'fund_source',
                    'supplier': 'supplier',
                    'project_name': 'project_name',
                    'remarks': 'remarks',
                    'is_returned': 'is_returned (boolean)',
                    'is_archived': 'is_archived (boolean)',
                }
            },
            'CATEGORY': {
                'old_field_examples': {
                    'id': 'id (AUTO_INCREMENT)',
                    'name/title': 'name'
                }
            },
            'STATUS': {
                'old_field_examples': {
                    'id': 'id (AUTO_INCREMENT)', 
                    'name/title': 'name'
                }
            }
        }
        
        for table, mapping in mappings.items():
            self.stdout.write(f'\n{table} FIELD MAPPING:')
            self.stdout.write(f"{'Old Field':<20} -> {'New Field':<30}")
            self.stdout.write('-' * 55)
            
            for old_field, new_field in mapping['old_field_examples'].items():
                self.stdout.write(f"{old_field:<20} -> {new_field:<30}")

        self.stdout.write('\nNOTES:')
        self.stdout.write('- All tables use AUTO_INCREMENT primary keys')
        self.stdout.write('- Foreign keys must reference existing records') 
        self.stdout.write('- Dates should be in YYYY-MM-DD format')
        self.stdout.write('- Boolean fields use 0/1 or FALSE/TRUE')
        self.stdout.write('- emp_id must reference valid users in auth_user_user table')
        self.stdout.write('- You may need to create placeholder users for missing employees')
