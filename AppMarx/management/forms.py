from django import forms
from lib import authenticate_user
from models import User, Website

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=40, min_length=4)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=40, min_length=4)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        # Only do something if both fields are valid so far.
        if password and password_confirmation:
            if password != password_confirmation:
                raise forms.ValidationError("Passwords do not match")
            
        return cleaned_data

class ForgetPasswordForm(forms.Form):
    email = forms.EmailField()
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=40)
    remember_me = forms.BooleanField(initial=True, required=False)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Incorrect email or password")
            ua = user.user_activation_set.all()
            if not ua or not ua[0].activated_at:
                raise forms.ValidationError("Please activate your account")
            if password:
                user = authenticate_user(email, password)
                if user is None:
                    raise forms.ValidationError("Incorrect email or password")
 
            
            # check if user activated his account
            ua = user.user_activation_set.all()
            if not ua or not ua[0].activated_at:
                raise forms.ValidationError("Please activate your account")
        # Always return the full collection of cleaned data.
        return cleaned_data

class SignupForm(forms.Form):
    fullname = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=40, min_length=4)
    url = forms.URLField(max_length=511)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        url = cleaned_data.get("url")
        # Check if account with email already exists
        if email:
            try: 
                User.objects.get(email=email)
            except User.DoesNotExist:
                return cleaned_data
            del cleaned_data["email"]
            raise forms.ValidationError("Email "+ email +" already exist")
        # Check if a VERIFIED site with same url exists
        if url:
            try: 
                Website.objects.get(url=url, is_verified=True)
            except Website.DoesNotExist:
                return cleaned_data
            self._errors["url"] = self.error_class( \
             ["Website '"+ url +"' already exist and verified"])
            del cleaned_data["url"]
        # Always return the full collection of cleaned data.
        return cleaned_data

# form for trial

class TryitForm(forms.Form):
    url = forms.URLField(max_length=511)