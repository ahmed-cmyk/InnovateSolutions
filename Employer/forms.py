import dns.exception
import dns.resolver
from django import forms
from django.contrib.auth.models import User
from upload_validator import FileTypeValidator

from .models import Employer


class InitialEmployerForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(InitialEmployerForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def usernameExists(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            return True
        return False

    def emailExists(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            return True
        return False

    def emailDomainExists(self):
        email = self.cleaned_data.get("email")
        domain = email.split('@')[1]
        try:
            dns.resolver.query(domain, 'MX')
            return True

        except dns.exception.DNSException:
            return False

    def samePasswords(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")

        if p1 != p2:
            return False
        return True


class EmployerForm(forms.ModelForm):
    logo = forms.ImageField(label='Logo', required=False, help_text="Only jpeg or png file formats allowed.",
                            validators=[FileTypeValidator(
                                allowed_types=['image/jpeg', 'image/png']
                            )])
    company_name = forms.CharField(max_length=50, label='Company Name', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    company_description = forms.CharField(label='Company Description', required=False, widget=forms.Textarea)
    phone_number = forms.CharField(label="Contact Number", required=False, max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;', 'id': "num"}))

    class Meta:
        model = Employer
        exclude = ['user', 'employer_id']


class EmployerAccVerificationForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['user', 'is_active']