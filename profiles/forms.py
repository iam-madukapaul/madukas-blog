from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user','username', 'email']

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Enter password', widget=forms.PasswordInput)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Email already exist!')
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        help_texts = {
            'username': None,
        }

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']