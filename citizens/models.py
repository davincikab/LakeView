from django.db import models
from django.utils import timezone
from django.urls import reverse
import uuid

class Person(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    person_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    surname = models.CharField(max_length=50, default="")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(choices=GENDER, max_length=10)
    dob = models.DateField("Date of Birth", auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        pass

    def get_person(self):
        return self.first_name+' '+self.last_name
        # return reverse("_detail", kwargs={"pk": self.pk})

class Citizen(models.Model):
    id_number = models.PositiveIntegerField(primary_key=True,verbose_name="Identification Number", unique=True)
    person = models.OneToOneField("Person", on_delete=models.CASCADE)
    location = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, blank=True)
    phone_number = models.CharField("Phone Number", max_length=12, blank=True, default='0704893840')
    voting_centre = models.CharField('Voting Centre', max_length=50, default='Unity Primary School')
    uploaded_to_google = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id_number) + ' '+ self.person.first_name

    def validate_id_number(self):
        #Ensure it is 8 character long
        if len(str(self.id_number)) != 8:
            raise ValueError("Id Number should be 8 character long")
        return self.id_number

    def validate_phone_number(self):
        size = len(str(self.id_number))
        if size < 10 or size > 13:
            raise ValueError("Invalid Phone Number")

        return self.phone_number
    
    def get_absolute_url(self):
        return reverse("citizen-detail", kwargs={"pk": self.pk})
        
    class Meta:
        verbose_name= 'Citizen'
        verbose_name_plural = 'Citizens'

class Messages(models.Model):
    ISSUE = (
        ('CT','Complaint'),
        ('CO','Concern'),
        ('OT','Others')
    )

    user = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='messages')
    date_created = models.DateTimeField(auto_now=True, auto_now_add=False)
    content = models.TextField()
    is_sorted = models.BooleanField(default=False)
    date_sorted = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now())
    type_of_isssue = models.CharField(choices=ISSUE, max_length=10)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.content 

    def get_absolute_url(self):
        return reverse("citizen-detail", kwargs={"pk": self.user.id_number})

# class Membership(models.Model):
#     pass

class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(Citizen)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("group-detail", kwargs={"pk": self.pk})
    
    def get_members(self):
        return self.members.all()

class GroupEvents(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(default="")
    venue = models.CharField("Event Venue", max_length=150)
    time = models.DateTimeField(auto_now=False, auto_now_add=False)
    attendants_count = models.IntegerField('Number of Attendants',default=0)

    class Meta:
        verbose_name = 'Group Event'
        verbose_name_plural = "Group Events"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("group-detail", kwargs={"pk": self.group.pk})
    
class Student(models.Model):
    person = models.OneToOneField("Person", on_delete=models.CASCADE)
    admission_number = models.IntegerField()
    school = models.CharField(max_length=150)
    form = models.CharField(max_length=50)
    is_sponsored = models.BooleanField("Sponsored Students", default=False)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
    
    def __str__(self):
        return self.person.get_person() + ' ' + str(self.admission_number)
    
    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})
    

class Bursary(models.Model):
    bursary_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey("Citizen", on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    date_issued = models.DateField(auto_now=False, auto_now_add=False)
    amount_awarded = models.IntegerField(default =0)

    class Meta:
        verbose_name = "Bursary"
        verbose_name_plural = "Bursary"

    def __str__(self):
        return self.parent.person.get_person() 

    def get_absolute_url(self):
        return reverse("bursary-list")


class College(models.Model):
    citizen = models.OneToOneField("Citizen", on_delete=models.CASCADE)
    collage_name = models.CharField( max_length=50)
    college_location = models.CharField(max_length=50)
    date_enrolled = models.DateField("Enrollement Date", auto_now=False, auto_now_add=False)
    date_completed = models.DateField("Completion Date", auto_now=False, auto_now_add=False, blank=True, default=timezone.now())
    course = models.CharField(max_length=50)
    duration = models.IntegerField("Period of Years")
    is_dropout = models.BooleanField(default=False)

    class Meta:
        verbose_name = "College"
        verbose_name_plural = "Colleges"

    def __str__(self):
        return self.citizen.person.first_name

    def get_absolute_url(self):
        return reverse("college-list")

# Sponsored Students
class SponsoredStudent(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Sponsored Student"
        verbose_name_plural = "Sponsored Students"

    def __str__(self):
        return str(self.student)

    def get_absolute_url(self):
        pass
        # return reverse("SponsoredStudent_detail", kwargs={"pk": self.pk})

# Team Members
class Results(models.Model):
    student = models.ForeignKey("Student",on_delete=models.CASCADE)
    term = models.IntegerField()
    year = models.IntegerField()
    grade = models.CharField(max_length=2)
    form = models.IntegerField(default=2)
    remarks = models.TextField()
    
    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"

    def __str__(self):
        return str(self.student)

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.student.pk})

# Events
class Events(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(default="")
    venue = models.CharField("Event Venue", max_length=150)
    time = models.DateTimeField(auto_now=False, auto_now_add=False)
    attendants_count = models.IntegerField('Number of Attendants',default=0)    

    class Meta:
        verbose_name = "Events"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("citizen-home")

# NCA
class NCA(models.Model):
    citizen = models.OneToOneField("Citizen", on_delete=models.CASCADE)
    processing_status = models.BooleanField(default=True)  

    class Meta:
        verbose_name = "National Contruction Authority"
        verbose_name_plural = "National Contruction Authority"

    def __str__(self):
        return str(self.citizen)

    def get_absolute_url(self):
        return reverse("nca-list")

# NHIF
class Nhif(models.Model):
    citizen = models.OneToOneField("Citizen", on_delete=models.CASCADE)
    ispending = models.BooleanField("Pending Status",default=False)
    
    class Meta:
        verbose_name = "NHIF"
        verbose_name_plural = "NHIF"

    def __str__(self):
        return str(self.citizen)

    def get_absolute_url(self):
        return reverse("nhif_list")

# Self Help Groups
class SelfHelpGroup(models.Model):
    name = models.CharField(max_length=50)
    reg_no = models.CharField("Registration Number", max_length=150) 
    location = models.CharField(max_length=50)   
    phone_number = models.CharField("Mobile Phone Number", max_length=50)

    class Meta:
        verbose_name = "Self Help Group"
        verbose_name_plural = "Self Help Groups"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("selfgroup")

# Projects
class Project(models.Model):
    name = models.CharField("Project Name", max_length=50)
    initiation_date = models.DateField("Initiation Date", auto_now=False, auto_now_add=False)
    project_budget = models.IntegerField()
    completion_date = models.DateField("Completion Date", auto_now=False, auto_now_add=False)
    contractor = models.CharField("Contractor Name", max_length=50)
    project_description = models.TextField("Project Description")
    completion_status = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project-list", kwargs={"pk": self.pk})

# Curiculum Vitae
class CuriculumVitae(models.Model):
    citizen = models.OneToOneField("Citizen", on_delete=models.CASCADE)
    qualifications = models.TextField()
    class Meta:
        verbose_name = "Curiculum Vitae"
        verbose_name_plural = "Curiculum Vitae"

    def __str__(self):
        return str(self.citizen.id_number)

    def get_absolute_url(self):
        return reverse("cv-list")

class TeamMembers(models.Model):
    citizen = models.OneToOneField("Citizen", on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    area_allocated = models.CharField("Area Allocated", max_length=50)
    picture = models.ImageField(default='download.jpg', upload_to="teammembers")

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __st__(self):
        return self.role
    
    def get_success_url(self):
        return reverse('team-list')

class Testimonials(models.Model):
    name =  models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=400)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return self.name
# class Reports(models.Model):
#     week = models.CharField(max_length=50)

# Create groups: Bursary, NHIF, NCA
# ----------- COLLEGE, DRIVING -----------------
# VOTING CENTRE
