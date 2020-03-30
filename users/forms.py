from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserLoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Username'
  }))
  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control',
    'placeholder': 'Password'
  }))

  def clean(self, *args, **kwargs):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')

    if username and password:
      user = authenticate(username=username, password=password)

      if not user:
        raise forms.ValidationError('The user does not exist')
      if not user.check_password(password):
        raise forms.ValidationError('The password is incorrect')
      if not user.is_active:
        raise forms.ValidationError('The user is not active')
    return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
  username = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Username'
  }))
  email = forms.CharField(widget=forms.EmailInput(attrs={
    'class': 'form-control',
    'placeholder': 'someone@gmail.com'
  }))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control',
    'placeholder': 'Password'
  }))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control',
    'placeholder': 'Confirm Password'
  }))

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
  
  def clean(self, *args, **kwargs):
    username = self.cleaned_data.get('username')
    email = self.cleaned_data.get('email')
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')

    if password1 != password2:
      raise forms.ValidationError('The two passwords do not match')
    user_qs = User.objects.filter(username=username)
    if user_qs.exists():
      raise forms.ValidationError('The user already exist')
    email_qs = User.objects.filter(email=email)
    if email_qs.exists():
      raise forms.ValidationError('The email has already been taken')
    return super(UserRegisterForm, self).clean(*args, **kwargs)