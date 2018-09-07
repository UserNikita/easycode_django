from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, UsernameField
from django import forms
from .models import Profile, Comment


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'uk-input'


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'uk-input'


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-input uk-form-width-large'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-input uk-form-width-large'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'uk-input uk-form-width-large'}))

    class Meta:
        model = Profile
        fields = ('photo',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'uk-textarea', 'rows': 5}),
        }
