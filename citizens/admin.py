from django.contrib import admin
from .models import Messages, Citizen, Group, GroupEvents, College, Person, NCA,Nhif, SelfHelpGroup
from .models import Student, Events, Project, Bursary, Results, CuriculumVitae, TeamMembers,Testimonials

admin.site.register(Person)
admin.site.register(Citizen)
admin.site.register(Messages)
admin.site.register(Group)
admin.site.register(GroupEvents)
admin.site.register(College)
admin.site.register(NCA)
admin.site.register(Nhif)
admin.site.register(SelfHelpGroup)
admin.site.register(Student)
admin.site.register(Events)
admin.site.register(Project)
admin.site.register(Bursary)
admin.site.register(Results)
admin.site.register(CuriculumVitae)
admin.site.register(TeamMembers)
admin.site.register(Testimonials)
# Register your models here.
