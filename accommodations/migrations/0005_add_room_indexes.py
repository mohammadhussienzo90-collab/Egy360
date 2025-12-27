# Generated migration for Room model indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0004_add_performance_indexes'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='room',
            index=models.Index(fields=['accommodation'], name='room_accommodation_idx'),
        ),
        migrations.AddIndex(
            model_name='room',
            index=models.Index(fields=['accommodation', 'room_type'], name='room_acc_type_idx'),
        ),
        migrations.AddIndex(
            model_name='room',
            index=models.Index(fields=['available_rooms'], name='room_available_idx'),
        ),
    ]
