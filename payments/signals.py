# FILE: payment/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from .models import Payment, Booking


@receiver(post_save, sender=Payment)
def update_booking_payment_status(sender, instance, created, **kwargs):
    """
    Update booking payment status when payment is completed
    """
    if instance.status == 'completed' and instance.is_confirmed:
        booking = instance.booking
        booking.payment_status = 'paid'
        booking.save()


@receiver(pre_save, sender=Payment)
def log_payment_status_change(sender, instance, **kwargs):
    """
    Log payment status changes
    """
    if instance.pk:
        try:
            old_instance = Payment.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                # Log status change
                TransactionLog.objects.create(
                    payment=instance,
                    transaction_id=f"STATUS_CHANGE_{instance.payment_number}",
                    status=instance.status,
                    amount=instance.amount,
                    description=f"Payment status changed from {old_instance.status} to {instance.status}"
                )
        except Payment.DoesNotExist:
            pass