from django.forms import ModelForm
from .models import Citizen, Student, College, NCA, Nhif,Student,Person

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = "__all__"


class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['person']

class CitizenForm(ModelForm):
    class Meta:
        model = Citizen
        exclude = ['person']


class CollegeForm(ModelForm):
    class Meta:
        model = College
        exclude = ['citizen']