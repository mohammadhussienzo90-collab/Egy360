# bookings/forms.py
from django import forms
from .models import Booking


class BookingInquiryForm(forms.Form):
    """Form for booking inquiry/checkout"""

    # Dates
    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'required': True
        })
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'required': True
        })
    )

    # Guest details
    number_of_guests = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 20
        })
    )
    number_of_rooms = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 10
        })
    )

    # Contact information
    contact_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    contact_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    contact_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+20 123 456 7890'
        })
    )

    # Special requests
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any special requests or notes...'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')

        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError(
                    "Check-out date must be after check-in date."
                )

        return cleaned_data


class TourBookingForm(forms.Form):
    """Form for tour booking"""

    tour_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'required': True
        })
    )

    number_of_participants = forms.IntegerField(
        min_value=1,
        max_value=50,
        initial=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 50
        })
    )

    # Contact information
    contact_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    contact_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    contact_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+20 123 456 7890'
        })
    )

    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Dietary requirements, mobility needs, etc...'
        })
    )
