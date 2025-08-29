from django import forms
from .models import CurrencyItem

class CurrencyItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make front and back images required for new items only
        if not self.instance.pk:  # New item
            self.fields['front_image'].required = True
            self.fields['back_image'].required = True
    
    class Meta:
        model = CurrencyItem
        fields = ['title', 'item_type', 'year', 'denomination', 'material', 
                 'issuing_authority', 'description', 'front_image', 'back_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mughal Silver Rupee'}),
            'item_type': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1947'}),
            'denomination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1 Rupee'}),
            'material': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Silver, Copper-Nickel'}),
            'issuing_authority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reserve Bank of India'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'front_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'back_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class SearchFilterForm(forms.Form):
    search = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Search...', 
            'class': 'search-input'
        })
    )
    item_type = forms.ChoiceField(
        choices=[('', 'All Types')] + CurrencyItem.ITEM_TYPES, 
        required=False, 
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    year_from = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(attrs={
            'placeholder': 'From Year', 
            'class': 'year-input'
        })
    )
    year_to = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(attrs={
            'placeholder': 'To Year', 
            'class': 'year-input'
        })
    )
