from django.contrib import admin
from .models import Messages, Citizen, Group, GroupEvents

admin.site.register(Citizen)
admin.site.register(Messages)
admin.site.register(Group)
admin.site.register(GroupEvents)
# Register your models here.
