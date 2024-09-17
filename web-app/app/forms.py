from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name', widget=forms.TextInput())
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput())


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

