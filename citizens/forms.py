from django import forms
from .models import Citizen, Student, College, NCA, Nhif,Student,Person, Results, Bursary

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['person']

class CitizenForm(forms.ModelForm):
    class Meta:
        model = Citizen
        exclude = ['person']


class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        exclude = ['citizen']

class ResultsForm(forms.ModelForm):
    class Meta:
        model = Results
        exclude = ['student']

class BursaryForm(forms.ModelForm):
    class Meta:
        model = Bursary
        exclude = ['citizen','student']