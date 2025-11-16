"""
Registration Forms for Different User Types
Path: accounts/forms.py

Three registration forms:
1. Customer Registration (tourists)
2. Property Owner Registration (hotels/tours)
3. Profile Update Form
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class CustomerRegistrationForm(UserCreationForm):
    """
    Registration form for customers (tourists)
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    # Profile fields
    phone_number = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Update profile
            profile = user.profile
            profile.user_type = 'customer'
            profile.phone_number = self.cleaned_data.get('phone_number', '')
            profile.country = self.cleaned_data.get('country', '')
            profile.city = self.cleaned_data.get('city', '')
            profile.save()

        return user


class PropertyOwnerRegistrationForm(UserCreationForm):
    """
    Registration form for property owners/managers
    More detailed - requires business information
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    # Contact fields
    phone_number = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

    # Business fields
    business_name = forms.CharField(max_length=200, required=True)
    business_license = forms.CharField(
        max_length=100,
        required=False,
        help_text="Optional - but required for verification"
    )
    tax_id = forms.CharField(
        max_length=100,
        required=False,
        help_text="Optional - but required for payments"
    )

    # Verification document
    verification_document = forms.FileField(
        required=False,
        help_text="Upload business license, ID, or other verification document"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            if field_name == 'verification_document':
                field.widget.attrs['class'] = 'form-control-file'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Update profile with business info
            profile = user.profile
            profile.user_type = 'property_owner'
            profile.phone_number = self.cleaned_data['phone_number']
            profile.country = self.cleaned_data['country']
            profile.city = self.cleaned_data['city']
            profile.address = self.cleaned_data['address']
            profile.business_name = self.cleaned_data['business_name']
            profile.business_license = self.cleaned_data.get('business_license', '')
            profile.tax_id = self.cleaned_data.get('tax_id', '')

            if self.cleaned_data.get('verification_document'):
                profile.verification_document = self.cleaned_data['verification_document']

            profile.save()

        return user


class UserProfileUpdateForm(forms.ModelForm):
    """
    Form for users to update their profile
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 'country', 'city', 'address',
            'profile_picture', 'bio', 'date_of_birth'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            if field_name == 'profile_picture':
                field.widget.attrs['class'] = 'form-control-file'
            else:
                field.widget.attrs['class'] = 'form-control'

        # Add user fields if profile exists
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Update user fields
        user = profile.user
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile.save()

        return profile


class PropertyOwnerProfileUpdateForm(UserProfileUpdateForm):
    """
    Extended profile update form for property owners
    Includes business information
    """

    class Meta(UserProfileUpdateForm.Meta):
        fields = UserProfileUpdateForm.Meta.fields + [
            'business_name', 'business_license', 'tax_id'
        ]