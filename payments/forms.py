# FILE: payments/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Refund, PaymentMethod


class PaymentMethodForm(forms.Form):
    payment_method = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
        widget=forms.RadioSelect,
        label=_('Select Payment Method')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].queryset = PaymentMethod.objects.filter(is_active=True)


class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['reason', 'reason_details']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'reason_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'reason': _('Refund Reason'),
            'reason_details': _('Additional Details'),
        }