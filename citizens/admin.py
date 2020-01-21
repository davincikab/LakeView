from django.contrib import admin
from .models import Messages, Citizen, Group

admin.site.register(Citizen)
admin.site.register(Messages)
admin.site.register(Group)
# Register your models here.
