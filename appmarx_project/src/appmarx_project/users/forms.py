from django import forms
from appmarx_project.users.lib import authenticate_user
from appmarx_project.users.models import User
from appmarx_project.websites.models import Website

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=40)
    remember_me = forms.BooleanField(initial=True, required=False)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # Only do something if both fields are valid so far.
        if email and password:
            user = authenticate_user(email, password)
            if user is None:
                raise forms.ValidationError("Incorrect email or password")

        # Always return the full collection of cleaned data.
        return cleaned_data

class SignupForm(forms.Form):
    fullname = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=40)
    URL = forms.URLField(max_length=511)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        URL = cleaned_data.get("URL")
        # Check if account with email already exists
        if email:
            try: 
                User.objects.get(email=email)
            except User.DoesNotExist:
                return cleaned_data
            del cleaned_data["email"]
            raise forms.ValidationError("Email "+ email +" already exist")
        # Check if a VERIFIED site with same URL exists
        if URL:
            try: 
                Website.objects.get(URL=URL, is_verified=True)
            except Website.DoesNotExist:
                return cleaned_data
            self._errors["URL"] = self.error_class( \
             ["Website '"+ URL +"' already exist and verified"])
            del cleaned_data["URL"]
        # Always return the full collection of cleaned data.
        return cleaned_data