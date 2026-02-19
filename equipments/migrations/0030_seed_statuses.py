# Generated manually for seeding default statuses

from django.db import migrations


def create_default_statuses(apps, schema_editor):
    """Create default equipment statuses"""
    Status = apps.get_model('equipments', 'Status')
    
    default_statuses = [
        'Active',
        'Maintenance',
        'Damaged',
        'Lost',
        'Stored',
    ]
    
    for status_name in default_statuses:
        Status.objects.get_or_create(name=status_name)


def remove_default_statuses(apps, schema_editor):
    """Remove default statuses (reverse migration)"""
    Status = apps.get_model('equipments', 'Status')
    
    default_statuses = [
        'Active',
        'Maintenance',
        'Damaged',
        'Lost',
        'Stored',
    ]
    
    Status.objects.filter(name__in=default_statuses).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0029_seed_categories'),
    ]

    operations = [
        migrations.RunPython(create_default_statuses, remove_default_statuses),
    ]
