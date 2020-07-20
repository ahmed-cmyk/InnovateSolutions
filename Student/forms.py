from re import search

# Note: we need dnspython for this to work
import datetime
import dns.exception
import dns.resolver
from django import forms
from django.contrib.auth.models import User
from django.forms import SelectDateWidget
from upload_validator import FileTypeValidator

from Accounts.views import isValidated, number_symbol_exists
from Home.models import Skill, Major
from .models import Student, StudentJobApplication


class InitialStudentForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Student Email Address')
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

    # password1.disabled = True
    def save(self, commit=True):
        user = super(InitialStudentForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    # def clean_first_name(self):
    #     first_name = self.cleaned_data.get('first_name')
    #     if number_symbol_exists(first_name):  # checks if number/symbol exists in string
    #         raise forms.ValidationError("You cannot have numbers in your first name.")
    #
    #     return first_name
    #
    # def clean_last_name(self):
    #     last_name = self.cleaned_data.get('last_name')
    #     if number_symbol_exists(last_name):  # checks if number/symbol exists in string
    #         raise forms.ValidationError('You cannot have numbers in your last name.')
    #
    #     return last_name
    #
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(username=email).exists():
    #         raise forms.ValidationError("This email is already being used.")
    #     elif not search("@student.murdoch.edu.au", email):
    #         raise forms.ValidationError("This is not a valid student email.")
    #
    #     return email
    #
    # def clean_password1(self):
    #     password1 = self.cleaned_data.get('password1')
    #     if not isValidated(password1):
    #         raise forms.ValidationError('Password is not valid.')
    #
    #     return password1
    #
    # def clean_password2(self):
    #     password2 = self.cleaned_data.get('password2')
    #     if not isValidated(password2):
    #         raise forms.ValidationError('Password is not valid.')
    #
    #     return password2
    #
    # # def usernameExists(self):
    # #     email = self.cleaned_data.get("email")
    # #     if User.objects.filter(username=email).exists():
    # #         raise forms.ValidationError("Please enter an email.")
    # #     return False
    # #
    # # def emailExists(self):
    # #     email = self.cleaned_data.get("email")
    # #     if User.objects.filter(email=email).exists():
    # #         return True
    # #     return False
    #
    # def email_domain_exists(self):
    #     email = self.cleaned_data.get("email")
    #     domain = email.split('@')[1]
    #     try:
    #         dns.resolver.query(domain, 'MX')
    #         return True
    #
    #     except dns.exception.DNSException:
    #         return False
    #
    # def same_passwords(self):
    #     p1 = self.cleaned_data.get("password1")
    #     p2 = self.cleaned_data.get("password2")
    #
    #     if p1 != p2:
    #         return False
    #     return True


class StudentForm(forms.ModelForm):
    year = datetime.date.today().year
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    gender = forms.ChoiceField(choices=gender_choices,
                               label='Gender',
                               required=True,
                               widget=forms.RadioSelect(attrs={'class': 'custom-select'}))
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True,
                                    label="Date Of Birth")
    student_id = forms.CharField(label='Student ID', max_length=8, min_length=8, required=True)
    expected_graduation_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True,
                                               label="Expected Graduation Date")
    personal_email = forms.EmailField(label='Personal Email Address')
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                            label='Skills*',
                                            widget=forms.CheckboxSelectMultiple,
                                            required=True)
    majors = forms.ModelMultipleChoiceField(queryset=Major.objects.all(),
                                            label='Major',
                                            widget=forms.CheckboxSelectMultiple,
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
        model = Student
        exclude = ['user', 'jobs_applied']


class EditStudentProfileInitialForm(forms.ModelForm):
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


class EditStudentProfileForm(StudentForm):
    class Meta:
        model = Student
        exclude = ['user', 'jobs_applied', 'student_id']

    def __init__(self, *args, **kwargs):
        super(EditStudentProfileForm, self).__init__(*args, **kwargs)
        self.fields.pop('student_id')


class StudentJobApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentJobApplication
        fields = ['job_id', 'applied']
