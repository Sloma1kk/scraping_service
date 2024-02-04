from django import forms
from .models import *


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, to_field_name='slug',
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Город')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), required=False, to_field_name='slug',
                                      widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность')
