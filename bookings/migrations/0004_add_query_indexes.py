# Generated migration for additional Booking indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_add_payment_status'),
    ]

    operations = [
        # Additional composite indexes for common queries
        migrations.AddIndex(
            model_name='booking',
            index=models.Index(fields=['user', 'status', 'created_at'], name='booking_user_filter_idx'),
        ),
        migrations.AddIndex(
            model_name='booking',
            index=models.Index(fields=['status', 'payment_status'], name='booking_status_pay_idx'),
        ),
        migrations.AddIndex(
            model_name='booking',
            index=models.Index(fields=['created_at'], name='booking_created_idx'),
        ),
    ]
