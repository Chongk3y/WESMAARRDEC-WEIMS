# Generated manually for seeding default categories

from django.db import migrations


def create_default_categories(apps, schema_editor):
    """Create default equipment categories"""
    Category = apps.get_model('equipments', 'Category')
    
    default_categories = [
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
    
    for category_name in default_categories:
        Category.objects.get_or_create(name=category_name)


def remove_default_categories(apps, schema_editor):
    """Remove default categories (reverse migration)"""
    Category = apps.get_model('equipments', 'Category')
    
    default_categories = [
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
    
    Category.objects.filter(name__in=default_categories).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0028_equipmenthistory_reason'),
    ]

    operations = [
        migrations.RunPython(create_default_categories, remove_default_categories),
    ]
