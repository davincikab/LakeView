from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, id_number, password=None):
        if not id_number:
            raise ValueError("User must have and id number")
        user = self.model(
            id_number=id_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_number, password):
        """
        Create a superuser with the following details
        """
        user = self.create_user(
            id_number,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male')
    )

    id_number = models.PositiveIntegerField(
        verbose_name="Identification Number", unique=True)
    surname = models.CharField('Surname', max_length=50)
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    location = models.CharField(max_length=150)
    email = models.EmailField(max_length=255)
    gender = models.CharField(choices=GENDER, max_length=50)
    phone_number = models.PositiveIntegerField("Phone Number" ,blank=True, default='0704893840')
    dob = models.DateField('Date of Birth', auto_now=False, auto_now_add=False, default=timezone.now())
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'id_number'
    # REQUIRED_FIELDS = ['']

    def __str__(self):
        return str(self.id_number)
    
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
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


