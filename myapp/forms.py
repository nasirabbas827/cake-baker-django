from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'age','date_of_birth', 'gender', 'phone_number', 'address', 'profile_picture']

from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_picture']

from .models import CustomizationRequest

class CustomizationRequestForm(forms.ModelForm):
    class Meta:
        model = CustomizationRequest
        fields = ['size', 'design_details', 'additional_description']

        widgets = {
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'design_details': forms.Textarea(attrs={'class': 'form-control'}),
            'additional_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }