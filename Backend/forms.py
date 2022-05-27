from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm')

    username = forms.CharField(
            min_length=3,
            max_length=20,
            label='Username',
            widget=forms.TextInput(
                    attrs={'placeholder': 'Username'},
            ),
    )

    password = forms.CharField(
            min_length=3,
            max_length=20,
            label='Password',
            widget=forms.PasswordInput(
                    attrs={'placeholder': 'Password'},
            ),
    )

    password_confirm = forms.CharField(
            min_length=3,
            max_length=20,
            label='Password confirmation',
            widget=forms.PasswordInput(
                    attrs={'placeholder': 'Password again'},
            ),
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError('Passwords not equals each other!!!')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        if commit:
            user.save()
        return user
