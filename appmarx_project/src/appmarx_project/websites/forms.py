from django import forms

class TryitForm(forms.Form):
    URL = forms.URLField(max_length=511)