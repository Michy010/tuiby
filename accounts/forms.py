from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email'
    }))
    class meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter username Eg Msita, Msita@11',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter password Eg ABCB#123',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password',
        })


    def save(self, commit = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user