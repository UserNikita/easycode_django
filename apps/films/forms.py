from django import forms

from .models import Film


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'poster': forms.TextInput(attrs={'class': 'form-control'}),
            'kinopoisk_url': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'placeholder': ''}),
        }
