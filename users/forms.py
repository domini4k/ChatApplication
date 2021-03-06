from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)
User = get_user_model()


# These forms are used to authenticate and register users.
# There are a few exceptions added to validate proper data for example:
# if User is trying to use username which is being use an exception occurs.
# In this particular part of app the "super()" function is being used.
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Invalid username or password. Try again', code='invalid')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_confirm'
        ]

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Passwords must match', code='match')
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError('This username is being used. Try again', code='used')
        return super(UserRegisterForm, self).clean()
