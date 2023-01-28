from django import forms
from app.models import Customer

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'zipcode', 'state']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        'state':forms.Select(attrs={'class':'form-control'}),
        }
