import dns.exception
import dns.resolver
from django import forms
from django.contrib.auth.models import User
from upload_validator import FileTypeValidator

from .models import Alumni, AlumniJobApplication
from Home.models import Skill

class InitialAlumniForm(forms.ModelForm):
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
	gender_choices = [
	('Male', 'Male'),
	('Female', 'Female')
	]
	gender = forms.ChoiceField(choices=gender_choices,label='Gender',required=True,widget=forms.RadioSelect(attrs={'class': 'custom-select'}))
	date_of_birth = forms.DateField(
    	required=True,
    	label='Date of Birth',
    	widget=forms.DateInput(attrs={
    		'class': 'datepicker form-control-text',
    		'placeholder': 'YYYY-MM-DD',
    		'autocomplete': 'off'}))
	skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                        label='Skill',
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
		model = Alumni
		exclude = ['user', 'jobs_applied']


class EditAlumniProfileInitialForm(forms.ModelForm):
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