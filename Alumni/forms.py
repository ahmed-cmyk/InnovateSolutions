import datetime
import dns.exception
import dns.resolver
from django import forms
from django.contrib.auth.models import User
from upload_validator import FileTypeValidator

from .models import Alumni, AlumniJobApplication
from Home.models import Skill, Major


class InitialAlumniForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Personal Email Address', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,
                                help_text="The password must contain a combination of alphabets and numbers and "
                                          "should have a minimum length of 8 characters")
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
        labels = (
            {'first_name': 'First Name'},
            {'last_name': 'Last Name'},
        )

    def save(self, commit=True):
        user = super(InitialAlumniForm, self).save(commit=False)
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


class AlumniForm(forms.ModelForm):
    year = datetime.date.today().year
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    gender = forms.ChoiceField(choices=gender_choices, label='Gender', required=True,
                               widget=forms.RadioSelect(attrs={'class': 'custom-select'}))
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True,
                                    help_text="You should be at least 16 years old")
    student_id = forms.CharField(label='Student ID', max_length=8, min_length=8, required=False)
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                            label='Skills*',
                                            widget=forms.CheckboxSelectMultiple(attrs={'id':'skills'}),
                                            required=True)
    majors = forms.ModelMultipleChoiceField(queryset=Major.objects.all(),
                                            label='Major(s)*',
                                            widget=forms.CheckboxSelectMultiple(attrs={'id':'majors'}),
                                            required=True)
    dp = forms.ImageField(label='Select a profile picture (only jpeg and png file formats allowed)',
                          required=False,
                          validators=[FileTypeValidator(
                              allowed_types=['image/jpeg', 'image/png']
                          )])
    cv = forms.FileField(allow_empty_file=False,
                         label='Attach CV (only PDF, docx, and doc file formats allowed)',
                         validators=[FileTypeValidator(
                             allowed_types=[
                                 "application/pdf",
                                 "application/msword",
                                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
                         )])

    class Meta:
        model = Alumni
        exclude = ['user', 'jobs_applied', 'is_active']


class EditAlumniProfileInitialForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True,
                                    help_text="You should be at least 16 years old")

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


class EditAlumniProfileForm(AlumniForm):
    class Meta:
        model = Alumni
        exclude = ['user', 'jobs_applied']


class AlumniJobApplicationForm(forms.ModelForm):
    class Meta:
        model = AlumniJobApplication
        fields = ['job_id', 'applied']
