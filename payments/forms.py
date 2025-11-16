# FILE: payment/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import PaymentRefund


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
        model = PaymentRefund
        fields = ['reason', 'description']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'reason': _('Refund Reason'),
            'description': _('Additional Details'),
        }