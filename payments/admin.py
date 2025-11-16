"""
Payments Admin - Corrected
Path: payments/admin.py

Fixed: Correct model imports (Transaction, not PaymentTransaction)
"""

from django.contrib import admin
from .models import (
    Payment,
    Refund,
    PaymentMethod,
    Invoice,
    Transaction
)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_reference', 'user', 'booking', 'payment_method', 'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'currency', 'created_at']
    search_fields = ['payment_reference', 'user__username', 'booking__booking_reference', 'transaction_id']
    readonly_fields = ['payment_reference', 'created_at', 'updated_at', 'processed_at', 'completed_at', 'failed_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_reference', 'booking', 'user')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'amount', 'currency', 'transaction_id', 'gateway')
        }),
        ('Status', {
            'fields': ('status', 'failure_reason')
        }),
        ('Additional Information', {
            'fields': ('description', 'payment_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at', 'completed_at', 'failed_at', 'updated_at')
        }),
    )

    actions = ['mark_as_completed', 'mark_as_failed']

    def mark_as_completed(self, request, queryset):
        for payment in queryset:
            payment.mark_completed()
        self.message_user(request, f"{queryset.count()} payments marked as completed.")
    mark_as_completed.short_description = "Mark selected payments as completed"

    def mark_as_failed(self, request, queryset):
        for payment in queryset:
            payment.mark_failed("Admin action")
        self.message_user(request, f"{queryset.count()} payments marked as failed.")
    mark_as_failed.short_description = "Mark selected payments as failed"


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['refund_reference', 'payment', 'amount', 'currency', 'reason', 'status', 'requested_at']
    list_filter = ['status', 'reason', 'requested_at']
    search_fields = ['refund_reference', 'payment__payment_reference', 'transaction_id']
    readonly_fields = ['refund_reference', 'requested_at', 'updated_at', 'processed_at', 'completed_at']
    date_hierarchy = 'requested_at'

    fieldsets = (
        ('Refund Information', {
            'fields': ('refund_reference', 'payment')
        }),
        ('Refund Details', {
            'fields': ('amount', 'currency', 'reason', 'reason_details', 'transaction_id')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Processing', {
            'fields': ('requested_by', 'processed_by')
        }),
        ('Timestamps', {
            'fields': ('requested_at', 'processed_at', 'completed_at', 'updated_at')
        }),
    )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_type', 'last_four_digits', 'is_default', 'is_active', 'created_at']
    list_filter = ['card_type', 'is_default', 'is_active', 'created_at']
    search_fields = ['user__username', 'card_holder_name', 'last_four_digits']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Card Details', {
            'fields': ('card_type', 'last_four_digits', 'card_holder_name', 'expiry_month', 'expiry_year')
        }),
        ('Gateway', {
            'fields': ('payment_token', 'gateway')
        }),
        ('Status', {
            'fields': ('is_default', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'payment', 'customer_name', 'total_amount', 'currency', 'issued_at']
    list_filter = ['issued_at']
    search_fields = ['invoice_number', 'customer_name', 'customer_email']
    readonly_fields = ['invoice_number', 'issued_at']
    date_hierarchy = 'issued_at'

    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'payment')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_address', 'customer_tax_id')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'discount_amount', 'total_amount', 'currency')
        }),
        ('Additional', {
            'fields': ('notes', 'pdf_file', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('issued_at',)
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_reference', 'transaction_type', 'user', 'amount', 'currency', 'created_at']
    list_filter = ['transaction_type', 'currency', 'created_at']
    search_fields = ['transaction_reference', 'user__username', 'description']
    readonly_fields = ['transaction_reference', 'created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Transaction Information', {
            'fields': ('transaction_reference', 'transaction_type')
        }),
        ('Related Records', {
            'fields': ('payment', 'refund', 'user')
        }),
        ('Amount', {
            'fields': ('amount', 'currency')
        }),
        ('Details', {
            'fields': ('description', 'notes')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )