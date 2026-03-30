from django import forms
from billing.models import Plan

class SchoolSignupForm(forms.Form):

    school_name = forms.CharField(max_length=100)

    subdomain = forms.CharField(max_length=50)

    admin_email = forms.EmailField()

    password = forms.CharField(widget=forms.PasswordInput)

    plan = forms.ModelChoiceField(
            queryset=Plan.objects.all(),
            empty_label="Select a Plan")