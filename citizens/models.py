from django.db import models
from django.utils import timezone
from django.urls import reverse

class Citizen(models.Model):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male')
    )

    id_number = models.PositiveIntegerField(primary_key=True,verbose_name="Identification Number", unique=True)
    surname = models.CharField('Surname', max_length=50, blank=True)
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    location = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, blank=True)
    gender = models.CharField(choices=GENDER, max_length=50)
    phone_number = models.CharField("Phone Number", max_length=12, blank=True, default='0704893840')
    dob = models.DateField('Date of Birth', auto_now=False, auto_now_add=False, default=timezone.now())
    voting_centre = models.CharField('Voting Centre', max_length=50, default='Unity Primary School')
    

    def __str__(self):
        return str(self.id_number) + ' '+ self.first_name

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

# class GroupEvents(models.Model):
#     group = models.ForeignKey("Group", on_delete=models.CASCADE)
#     title = models.CharField(max_length=150)
#     content = models.TextField(default="")
#     venue = models.CharField("Event Venue", max_length=150)
#     time = models.DateTimeField(auto_now=False, auto_now_add=False)

#     class Meta:
#         verbose_name = 'Group Event'
#         verbose_name_plural = "Group Events"

#     def __str__(self):
#         return self.title
    
    
        
    

# Create groups: Bursary, NHIF, NCA
# ----------- COLLEGE, DRIVING -----------------
# VOTING CENTRE
