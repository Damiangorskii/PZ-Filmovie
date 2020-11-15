from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from users.models import Profile


def ForbiddenUserName(value):
    forbidden_user_name = ['admin', 'css', 'js', 'authenticate', 'login',
    'logout', 'root', 'password', 'administrator', 'email', 'sql', 'insert', 'db', 'static', 'database',
    'python', 'detele', 'table']

    if value.lower() in forbidden_user_name:
        raise ValidationError('Invalid name for user!')

def InvalidUser(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('You cannot add special symbol in your username')

def UniqueEmail(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this email already exists')

def UniqueUser(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this username already exists')


class SignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True)
    first_name = forms.CharField(widget=forms.TextInput(), max_length=30, required=True)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=30, required=True)
    email = forms.CharField(widget=forms.EmailInput(), max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirm your password')

    class Meta:
        model = User
        fields=('username', 'first_name', 'last_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUserName)
        self.fields['username'].validators.append(InvalidUser)
        self.fields['username'].validators.append(UniqueUser)
        self.fields['email'].validators.append(UniqueEmail)

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            self._errors['password'] = self.error_class(['Password do not match!'])

        return self.cleaned_data



class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(), label='Old password', required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(), label='New password', required=True)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm new password', required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_new_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        condirm_new_password = self.cleaned_data.get('confirm_new_password')
        user = User.objects.get(pk=id)

        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class(['Old password do not match'])

        if new_password != condirm_new_password:
            self._errors['new_password'] = self.error_class(['Passwords do not match'])
        
        return self.cleaned_data


class EditProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    location = forms.CharField(widget=forms.TextInput(), max_length=25, required=False)
    bio = forms.CharField(widget=forms.TextInput(), max_length=200, required=False)

    class Meta:
        model = Profile
        fields = ('picture', 'first_name', 'last_name', 'location', 'bio')
