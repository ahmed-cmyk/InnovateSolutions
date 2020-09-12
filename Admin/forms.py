from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from upload_validator import FileTypeValidator

from .models import Admin
from Home.models import Job, JobType, Major, Skill, Industry
from Alumni.models import Alumni
from Student.models import Student
from Employer.models import Employer

import dns.resolver, dns.exception


class InitialAdminForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email Address', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(InitialAdminForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        content_type = [ContentType.objects.get_for_model(Industry), ContentType.objects.get_for_model(JobType),
                        ContentType.objects.get_for_model(Job), ContentType.objects.get_for_model(Major),
                        ContentType.objects.get_for_model(Skill), ContentType.objects.get_for_model(Employer),
                        ContentType.objects.get_for_model(Student), ContentType.objects.get_for_model(Alumni)]
        permissions = Permission.objects.filter(content_type__in=content_type)  # 14 industry, #15 jobtype, #16 skill, #18 job
        user.user_permissions.add(*permissions)
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


class AdminForm(forms.ModelForm):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={'class': 'custom-select'}))

    dp = forms.ImageField(label='Select a profile picture (only jpeg and png file formats allowed)', required=False,
                          validators=[FileTypeValidator(
                              allowed_types=['image/jpeg', 'image/png']
                          )])

    class Meta:
        model = Admin
        exclude = ['user', ]


class EditAdminProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name'
        )
        labels = (
            {'first_name': 'First Name'},
            {'last_name': 'Last Name'}
        )
        exclude = ['email', 'password1', 'password2']


class AddIndustryForm(forms.ModelForm):
    industry_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs=
                                                                                         {'class': 'form-control-text',
                                                                                          'style': 'resize:none;'}))


class Statistics(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'id':'start_date'}), required=True)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'id':'end_date'}), required=True)


class JobStats(forms.ModelForm):
    LOCATION_CHOICES = [
        ('--Select--', '--Select--'),
        ('Abu Dhabi', 'Abu Dhabi'),
        ('Dubai', 'Dubai'),
        ('Sharjah', 'Sharjah'),
        ('Umm al-Qaiwain', 'Umm al-Qaiwain'),
        ('Fujairah', 'Fujairah'),
        ('Ajman', 'Ajman'),
        ('Ra’s al-Khaimah', 'Ra’s al-Khaimah')
    ]
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'id':'start_date'}), required=True)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'id':'end_date'}), required=True)
    industry = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=Industry.objects.all().order_by('industry_name'),
        required=False,
        label="Industry"
    )
    job_type = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=JobType.objects.all(),
        required=False,
        label="Job Type"
    )
    location = forms.CharField(max_length=100, required=False, widget=forms.Select(choices=LOCATION_CHOICES))

    class Meta:
        model = Job
        fields = ['industry_id', 'job_type_id', 'location']

    def __init__(self, *args, **kwargs):
        super(JobStats, self).__init__(*args, **kwargs)
        self.fields['job_type'].required = False
        self.fields['industry'].required = False

class StudentStats(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'id':'start_date'}), required=True)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'id':'end_date'}), required=True)
    major = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=Major.objects.all().order_by('major_name'),
        required=False,
        label="Major"
    )
    skill = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=Skill.objects.all().order_by('skill_name'),
        required=False,
        label="Skills"
    )