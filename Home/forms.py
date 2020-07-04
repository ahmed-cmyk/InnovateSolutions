from django import forms
from Home.models import Job, Skill, JobType, Industry
from Student.models import Student
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from DjangoUnlimited import settings


class CreateJobForm(forms.Form):
    job_title = forms.CharField(label='*Job Title', max_length=100, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    description = forms.CharField(label='*Job Description', max_length=750, required=True, widget=forms.Textarea(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    duration = forms.IntegerField(label='*Duration (in months)')
    location = CountryField().formfield(blank_label='(Select country)')
    job_type_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=JobType.objects.all(),
        required = True,
        label="*Job Type"
    )
    salary = forms.FloatField(label="*Salary (AED per month)")
    skills = forms.ModelMultipleChoiceField(
        label='*Skill',
        widget=forms.CheckboxSelectMultiple,
        queryset=Skill.objects.all(),
        required = True
    )

    industry_id = forms.ModelChoiceField(
        label='*Industry',
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=Industry.objects.all(),
        required = True,
    )

    class Meta:
        model = Job
        exclude = ['posted_by', 'date_posted', 'status', 'date_closed']
        widgets = {'country': CountrySelectWidget()}


class EditJobForm(forms.ModelForm):
    job_title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    description = forms.CharField(label='Job Description', max_length=750, required=True, widget=forms.Textarea(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))

    duration = forms.IntegerField(label='Duration (in months)')
    location = forms.CharField(max_length = 100, required = True)
    job_type_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=JobType.objects.all(),
        required = True,
        label="Job Type"
    )
    salary = forms.FloatField(label="Salary (AED per month)")
    skills = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Skill.objects.all(),
        required = True
    )

    industry_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=Industry.objects.all(),
        required = True,
        label="Industry"
    )

    class Meta:
        model = Job
        exclude = ['posted_by', 'date_posted', 'date_closed', 'status']


class FilterJobForm(forms.ModelForm):
    min_duration = forms.IntegerField(required=False)
    max_duration = forms.IntegerField(required=False)
    location = CountryField().formfield(blank_label='(Select country)')
    job_type_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=JobType.objects.all(),
        required=False,
        label="Job Type"
    )
    min_salary = forms.FloatField(required=False)
    max_salary = forms.FloatField(required=False)

    industry_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=Industry.objects.all(),
        required=False,
        label="Industry"
    )

    class Meta:
        model = Job
        fields = ['min_duration', 'max_duration', 'location', 'job_type_id', 'min_salary', 'max_salary',
                  'industry_id']
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(FilterJobForm, self).__init__(*args, **kwargs)
        self.fields['job_type_id'].required = False
        self.fields['industry_id'].required = False
        self.fields['min_duration'].widget.attrs['placeholder'] = 'Min'
        self.fields['max_duration'].widget.attrs['placeholder'] = 'Max'
        self.fields['min_salary'].widget.attrs['placeholder'] = 'Min'
        self.fields['max_salary'].widget.attrs['placeholder'] = 'Min'


class FilterStudentForm(forms.Form):
    choices = [
        ('Current', 'Current'),
        ('Alumni', 'Alumni')
    ]
    alumni_status = forms.ChoiceField(required=False, label='Student Status', choices=choices,
                                       widget=forms.RadioSelect(attrs={'class': 'custom-select',
                                                                       'onClick': 'disable_fields(this.checked)'}))

    min_graduation_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False,
                                               label='Minimum Graduation Date',
                                               widget=forms.DateInput(attrs={
                                                   'class': 'datepicker form-control-text',
                                                   'placeholder': 'YYYY-MM-DD',
                                                   'autocomplete': 'off'
                                                }))
    max_graduation_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False,
                                          label='Maximum Graduation Date',
                                          widget=forms.DateInput(attrs={
                                              'class': 'datepicker form-control-text',
                                              'placeholder': 'YYYY-MM-DD',
                                              'autocomplete': 'off'
                                          }))

    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                            widget=forms.CheckboxSelectMultiple,
                                            required=True)

    class Meta:
        model = Student
        fields = ['alumni_status', 'skills']

    def __init__(self, *args, **kwargs):
        super(FilterStudentForm, self).__init__(*args, **kwargs)
        self.fields['min_graduation_date'].widget.attrs['placeholder'] = 'Min'
        self.fields['max_graduation_date'].widget.attrs['placeholder'] = 'Max'
