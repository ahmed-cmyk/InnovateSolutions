import dns.exception
import dns.resolver
from django import forms
from django.contrib.auth.models import User
from upload_validator import FileTypeValidator

from .models import Employer


class InitialEmployerForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,
                                help_text="The password must contain alphanumeric characters and should have a minimum of 6 characters")
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
    company_description = forms.CharField(label='Company Description', required=True, widget=forms.Textarea)
    company_website = forms.URLField(label='Company Description', required=True,
                                     help_text="Website should start with http or https")
    phone_number = forms.CharField(label="Contact Number", required=True, max_length=15,
                                   help_text="Phone number should have country code appended before it",
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control-text', 'style': 'resize:none;', 'id': "num"}), )
    contact_name = forms.CharField(max_length=50, label='Contact Name', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    trade_license = forms.FileField(allow_empty_file=False, label='Trade License',
                                    help_text="*Disclaimer: Please attach a copy of your registered trade license",
                                    validators=[FileTypeValidator(
                                        allowed_types=["image/*", "application/pdf", "application/msword",
                                                       "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
                                    )])

    class Meta:
        model = Employer
        exclude = ['user', 'employer_id', 'is_active']


class EditEmployerForm(forms.ModelForm):
    logo = forms.ImageField(label='Logo', required=False, help_text="Only jpeg or png file formats allowed.",
                            validators=[FileTypeValidator(
                                allowed_types=['image/jpeg', 'image/png']
                            )])
    company_name = forms.CharField(max_length=50, label='Company Name', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    company_description = forms.CharField(label='Company Description', required=True, widget=forms.Textarea)
    company_website = forms.URLField(label='Company Description', required=True,
                                     help_text="Website should start with http or https")
    phone_number = forms.CharField(label="Contact Number", required=True, max_length=15,
                                   help_text="Phone number should have country code appended before it",
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control-text', 'style': 'resize:none;', 'id': "num"}))
    contact_name = forms.CharField(max_length=50, label='Contact Name', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    trade_license = forms.FileField(allow_empty_file=False, label='Trade License', required=False,
                                    help_text="*Disclaimer: Please attach a copy of your registered trade license",
                                    validators=[FileTypeValidator(
                                        allowed_types=["image/*", "application/pdf", "application/msword",
                                                       "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
                                    )])

    class Meta:
        model = Employer
        exclude = ['user', 'employer_id', 'is_active']


class EmployerAccVerificationForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['user', 'is_active']
