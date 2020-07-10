from django import forms
from Home.models import Job, Skill, JobType, Industry
from Student.models import Student

from DjangoUnlimited import settings


class CreateJobForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        label='*Skill',
        widget=forms.CheckboxSelectMultiple,
        queryset=Skill.objects.all(),
        required=True
    )

    class Meta:
        model = Job
        exclude = ['posted_by', 'date_posted', 'status', 'date_closed']


class EditJobForm(CreateJobForm):
    class Meta:
        model = Job
        exclude = ['posted_by', 'date_posted', 'date_closed', 'status']


class FilterJobForm(forms.ModelForm):
    LOCATION_CHOICES = [
        ('Abu Dhabi', 'Abu Dhabi'),
        ('Dubai', 'Dubai'),
        ('Sharjah', 'Sharjah'),
        ('Umm al-Qaiwain', 'Umm al-Qaiwain'),
        ('Fujairah', 'Fujairah'),
        ('Ajman', 'Ajman'),
        ('Ra’s al-Khaimah', 'Ra’s al-Khaimah')
    ]
    min_duration = forms.IntegerField(required=False)
    max_duration = forms.IntegerField(required=False)
    location = forms.CharField(max_length=100, required=True, widget=forms.Select(choices=LOCATION_CHOICES))
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
                                      widget=forms.RadioSelect(attrs={'class': 'custom-select'}))
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
