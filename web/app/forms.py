from django import forms
from models import *
from django.forms import ModelForm, Form, ValidationError
from django.contrib.auth.forms import AuthenticationForm
from box import createProfFolder
import logging

class LogInForm(AuthenticationForm):
  username = forms.EmailField(max_length=30, label='Email',
    error_messages={'required': 'required', 'invalid': 'invalid email',})
  password = forms.CharField(widget=forms.PasswordInput, label="Password",
    error_messages={'required': 'required'})
  def clean(self):
    try:
      return super(LogInForm, self).clean()
    except ValidationError, err:
      if "username" in str(err) and "password" in str(err):
        raise ValidationError('Incorrect email/password combination')
      raise
	  
class SignUpForm(ModelForm):
  email = forms.EmailField(max_length=30, 
    error_messages={'required': 'required', 'invalid': 'invalid email',
    'unique': 'email is already being used',})
  password = forms.CharField(widget=forms.PasswordInput, label="Your Password",
    error_messages={'required': 'required'})
  def save(self, force_insert=False, force_update=False, commit=True):
    u = super(SignUpForm, self).save(commit=False)
    email = self.cleaned_data['email']
    password = self.cleaned_data['password']
    logging.warning(u.email[0:u.email.find('@')])
    u.box_id = int(createProfFolder(u.email[0:u.email.find('@')]))
	#gdocs id
    u.user = User.objects.create_user(email, email, password)
    if commit:
      u.save()
    return u
  class Meta:
    model = Professor
    fields = ('email', 'password',)