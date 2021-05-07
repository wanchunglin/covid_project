from django import forms
from .models import tempImage

class tempForm(forms.ModelForm):
    class Meta:
        model= tempImage
        fields = ["tempimg"]

