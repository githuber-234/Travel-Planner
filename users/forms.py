from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150, required=True, label="Full Name")

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name')

        user.first_name = full_name  

        if commit:
            user.save()
        return user
