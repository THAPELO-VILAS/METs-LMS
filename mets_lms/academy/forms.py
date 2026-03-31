from django import forms
from .models import Assignment, Project

class AssignmentUploadForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['file']  # Only allow students to upload files

class ProjectUploadForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['file']  # Only allow students to upload files