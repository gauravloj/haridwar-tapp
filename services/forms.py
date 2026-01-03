from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent'
        })
    )

    class Meta:
        model = Booking
        fields = ('customer_name', 'customer_email', 'customer_phone', 'customer_address', 'preferred_date', 'special_requests')
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent',
                'placeholder': 'Your Full Name'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent',
                'placeholder': 'your@email.com'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent',
                'placeholder': '+91-XXXXXXXXXX'
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent',
                'placeholder': 'Your Address',
                'rows': 3
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent',
                'placeholder': 'Any special requests (optional)',
                'rows': 3
            }),
        }
