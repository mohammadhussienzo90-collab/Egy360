# Generated migration for TourBooking and TourItinerary indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0003_add_performance_indexes'),
    ]

    operations = [
        # TourBooking indexes
        migrations.AddIndex(
            model_name='tourbooking',
            index=models.Index(fields=['tour'], name='tourbooking_tour_idx'),
        ),
        migrations.AddIndex(
            model_name='tourbooking',
            index=models.Index(fields=['user'], name='tourbooking_user_idx'),
        ),
        migrations.AddIndex(
            model_name='tourbooking',
            index=models.Index(fields=['status'], name='tourbooking_status_idx'),
        ),
        migrations.AddIndex(
            model_name='tourbooking',
            index=models.Index(fields=['tour', 'status', 'booking_date'], name='tourbooking_filter_idx'),
        ),
        migrations.AddIndex(
            model_name='tourbooking',
            index=models.Index(fields=['user', 'status'], name='tourbooking_user_status_idx'),
        ),
        # TourItinerary indexes
        migrations.AddIndex(
            model_name='touritinerary',
            index=models.Index(fields=['tour'], name='touritinerary_tour_idx'),
        ),
    ]
