from django import forms
from datetime import date, timedelta
from .models import CustomOrderRequest


class CustomOrderForm(forms.ModelForm):
    class Meta:
        model = CustomOrderRequest
        fields = [
            'customer_name',
            'email',
            'phone',
            'fulfillment_type',
            'delivery_address',
            'event_date',
            'servings_required',
            'flavor_preference',
            'dietary_requirements',
            'design_instructions',
            'reference_image',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400',
                'placeholder': '+27 82 000 0000'
            }),
            'fulfillment_type': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400 bg-white'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400',
                'rows': 2,
                'placeholder': 'Street Address & Suburb in Middelburg (e.g. Aerorand, Kanonkop)'
            }),
            'event_date': forms.DateInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400',
                'type': 'date',
                'min': (date.today() + timedelta(days=1)).isoformat()
            }),
            'servings_required': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400',
                'min': 1
            }),
            'flavor_preference': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400',
                'placeholder': 'e.g. Vanilla Sponge, Chocolate Ganache, Red Velvet'
            }),
            'dietary_requirements': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400',
                'placeholder': 'e.g. Eggless, Dairy-Free, Nut Allergy'
            }),
            'design_instructions': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-md px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400',
                'rows': 4,
                'placeholder': 'Describe your design idea, colors, wording, or theme...'
            }),
            'reference_image': forms.FileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-navy-950 file:text-white hover:file:bg-navy-900'
            }),
        }

    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date < date.today() + timedelta(days=1):
            raise forms.ValidationError("Orders require at least 24 hours advance notice.")
        return event_date