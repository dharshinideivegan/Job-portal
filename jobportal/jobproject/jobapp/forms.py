from django import forms
from .models import Job, JobApplication

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['applicant_name', 'applicant_email', 'resume']
