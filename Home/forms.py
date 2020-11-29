import datetime
from django import forms

from Home.models import Job, Skill, JobType, Industry, Major
from Student.models import Student
from Alumni.models import Alumni


class CreateJobForm(forms.ModelForm):
    DURATION = [
        ('--Select--', '--Select--'),
        ('Days', 'Days'),
        ('Weeks', 'Weeks'),
        ('Months', 'Months'),
        ('Permanent', 'Permanent'),
    ]

    skills = forms.ModelMultipleChoiceField(
        label='Skills Required*',
        widget=forms.CheckboxSelectMultiple(attrs={'onChange': 'checkOtherSkills(this)', 'id': 'skills'}),
        queryset=Skill.objects.all().order_by('skill_name'),
        required=True
    )

    other_skills = forms.CharField(
        label='Other Skills (Optional)',
        widget=forms.Textarea(attrs={'id': 'otherskills'}),
        required=False
    )

    duration_type = forms.CharField(max_length=10,
                                    widget=forms.Select(choices=DURATION,
                                                        attrs={'id': 'duration_type',
                                                               'onChange': 'toggleDuration(this)'}),
                                    required=True)
    duration = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'id': 'duration'}))

    class Meta:
        model = Job
        exclude = ['date_posted', 'status', 'date_closed']
        labels = {
            "duration_type": "Duration Type",
            "duration": "Duration",
            "salary_min": "Minimum Salary (AED)",
            "salary_max": "Maximum Salary (AED)",
            "industry_id": "Industry",
            "job_type_id": "Job Type"
        }

    def __init__(self, *args, **kwargs):
        super(CreateJobForm, self).__init__(*args, **kwargs)


class EditJobForm(CreateJobForm):
    class Meta:
        model = Job
        exclude = ['posted_by', 'date_posted', 'date_closed', 'status']
        labels = {
            "duration_type": "Duration Type",
            "duration": "Duration",
            "salary_min": "Minimum Salary (AED)",
            "salary_max": "Maximum Salary (AED)",
            "industry_id": "Industry",
            "job_type_id": "Job Type"
        }


class FilterJobForm(forms.ModelForm):
    LOCATION_CHOICES = [
        ('--Select--', '--Select--'),
        ('Abu Dhabi', 'Abu Dhabi'),
        ('Dubai', 'Dubai'),
        ('Sharjah', 'Sharjah'),
        ('Umm al-Qaiwain', 'Umm al-Qaiwain'),
        ('Fujairah', 'Fujairah'),
        ('Ajman', 'Ajman'),
        ('Ra’s al-Khaimah', 'Ra’s al-Khaimah'),
        ('Remote', 'Remote'),
    ]
    DURATION = [
        ('--Select--', '--Select--'),
        ('Days', 'Days'),
        ('Weeks', 'Weeks'),
        ('Months', 'Months'),
        ('Permanent', 'Permanent'),
    ]
    min_duration = forms.IntegerField(required=False)
    max_duration = forms.IntegerField(required=False)
    duration_type = forms.CharField(max_length=10, widget=forms.Select(choices=DURATION))
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


class FilterStudentForm(forms.ModelForm):
    year = datetime.date.today().year
    min_graduation_date = forms.DateField(label="Min Graduation Date", widget=forms.TextInput(attrs={'type': 'date'}),
                                          required=False)
    max_graduation_date = forms.DateField(label="Max Graduation Date", widget=forms.TextInput(attrs={'type': 'date'}),
                                          required=False)
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                            widget=forms.CheckboxSelectMultiple,
                                            required=True)
    majors = forms.ModelMultipleChoiceField(queryset=Major.objects.all(),
                                            widget=forms.CheckboxSelectMultiple,
                                            required=True)

    class Meta:
        model = Student
        fields = ['skills', 'majors']

    def __init__(self, *args, **kwargs):
        super(FilterStudentForm, self).__init__(*args, **kwargs)
        self.fields['min_graduation_date'].widget.attrs['placeholder'] = 'Min'
        self.fields['max_graduation_date'].widget.attrs['placeholder'] = 'Max'


class FilterAlumniForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                            widget=forms.CheckboxSelectMultiple,
                                            required=True)
    majors = forms.ModelMultipleChoiceField(queryset=Major.objects.all(),
                                            widget=forms.CheckboxSelectMultiple,
                                            required=True)

    class Meta:
        model = Alumni
        fields = ['skills', 'majors']
