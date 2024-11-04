from django import forms
from .models import Profile

class ProfileImageUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']  # This should match your Profile model's image field
