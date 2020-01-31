from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse, resolve

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.conf import settings
from django.utils import timezone
from django.core.serializers import serialize
from django.db.models import Count, Sum
from django.db.models import Q

from .models import Citizen, Messages, Group, GroupEvents, Bursary, \
    CuriculumVitae, College, Project, Person,NCA,Nhif, SelfHelpGroup,\
    Student, SponsoredStudent, Events, TeamMembers, Person, Results, Testimonials

from django.forms import formset_factory
from .forms import StudentForm, PersonForm, CitizenForm

import os
import csv
import json
from datetime import timedelta

# Change this to a class based view
@login_required(login_url='/user/login')
def home(request):
    context = {'data':'HOME IS WHERE MY HEART IS'}
    events = Events.objects.all()
    team_members = TeamMembers.objects.all()
    testimonials = Testimonials.objects.all()[:5]
    return render(request,'index.html', {'events':events,'teams':team_members,'testimonials':testimonials})


class CitizenListView(LoginRequiredMixin, ListView):
    model = Citizen
    context_object_name = 'citizens'
    template_name  = 'citizen/citizenlist.html'
    paginate_by = 7
    ordering = '-id_number'

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        results = searchCitizen(query)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mymessages"] = Messages.objects.filter(is_sorted=False).order_by('-date_created') 
        return context
    

class CitizenDetailView(LoginRequiredMixin, DetailView):
    model = Citizen
    context_object_name = "citizen"
    template_name = "citizen/citizendetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        print(self.kwargs['pk'])
        context['mymessages'] = Messages.objects.filter(user = self.kwargs['pk']).order_by('-date_created')
        context['members'] = Group.objects.filter(members=self.kwargs['pk'])
        context['groups'] = Group.objects.all()
        context['bursaries'] = Bursary.objects.filter(parent = self.kwargs['pk'])
        context['cv'] = CuriculumVitae.objects.filter(citizen=self.kwargs['pk'])
        context['nca'] = NCA.objects.filter(citizen=self.kwargs['pk'])
        # context['nhif'] = Nhif.objects.get(citizen=self.kwargs['pk'])
        return context
    
    def get_queryset(self):
        return super().get_queryset()

def create_person(data):
    surname = data.get('surname')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    gender = data.get('gender')
    dob = data.get('dob')
    person = Person.objects.create(surname=surname,first_name=first_name,last_name=last_name,gender=gender,dob=dob)

    return person

def create_citizen(request):
    if request.method == "POST":
        data = request.POST.copy()
        for key in ['surname', 'first_name','last_name','gender','dob']:
            del data[key]

        print(data)
        id_number = data.get('id_number')

        print(request.POST)
        form = CitizenForm(request.POST)
        if form.is_valid():
            person = create_person(request.POST)
            citizen = form.save(commit=False)
            citizen.person = person
            citizen.save()
            return HttpResponseRedirect(f'/citizen/{int(id_number)}/')
    else:
        form = CitizenForm()
    return render(request,"citizen/citizenupdate.html",{'form':form})

class CitizenCreateView(LoginRequiredMixin, CreateView):
    model = Citizen
    context_object_name = "citizen"
    template_name = "citizen/citizenupdate.html"
    fields = "__all__"

    def post(self, *args, **kwargs):
        form = self.get_form()
    def form_valid(self,form):
        pass
    def form_invalid(self,form):
        pass

class CitizenUpdateView(UpdateView,LoginRequiredMixin):
    model = Citizen
    context_object_name = 'citizen'
    template_name = "citizen/citizenupdate.html"
    fields = "__all__"


class CitizenDeleteView(LoginRequiredMixin,DeleteView):
    model = Citizen
    template_name = "citizen/citizendelete.html"
    success_url = reverse_lazy("list-view")


class MessagesCreateView(LoginRequiredMixin, CreateView):
    model = Messages
    fields = ['type_of_isssue', 'is_sorted','content', 'date_sorted']
    template_name = "message/messageupdate.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = Citizen.objects.get(pk = kwargs['id_number'])
            self.form_valid(form,user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form, user):
        self.object = form.save(commit=False)
        self.object.user =  user
        self.object.save()
    
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        # Add a message on field not creates
        return HttpResponseRedirect(self.get_success_url())


class MessagesUpdateView(LoginRequiredMixin, UpdateView):
    model = Messages
    template_name = "message/messagecreate.html"
    fields = "__all__"


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    context_object_name = "groups"
    template_name = 'groups/group_list.html'

    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = GroupEvents.objects.filter(time__gte = timezone.now()) 
        return context


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    context_object_name = "group"
    template_name = 'groups/group_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = GroupEvents.objects.filter(group = self.kwargs['pk'])
        return context
    
    def get_queryset(self):
        return super().get_queryset()


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = "groups/group_update.html"
    fields = "__all__"


class GroupCreateView(LoginRequiredMixin,CreateView):
    model = Group
    template_name = "groups/group_create.html"
    fields = "__all__"

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self,form):
        return HttpResponseRedirect(reverse('group-list'))

class GroupDeleteView(LoginRequiredMixin,DeleteView):
    model = Group
    template_name = "groups/group_delete.html"
    success_url = reverse_lazy("group-list")

# Group Events CRUD
class GroupEventsCreateView(LoginRequiredMixin, CreateView):
    model = GroupEvents
    fields = '__all__'
    template_name = 'events/event_createupdate.html'

# Update group Events
class GroupEventsUpdateView(LoginRequiredMixin, UpdateView):
    model = GroupEvents
    fields = '__all__'
    template_name = 'events/event_createupdate.html'

# Delete Events 
class GroupEventsDeleteView(LoginRequiredMixin, DeleteView):
    model = GroupEvents
    template_name = 'events/event_delete.html'
    success_url = reverse_lazy('group-list')

# Search a citizen using id number
def searchCitizen(id=None):
    if id == '' or id == None:
        results = Citizen.objects.all()
    else:
        results = Citizen.objects.filter(pk=id)
    return results

# Map the citizens data from the models to a csv file
@login_required(login_url='/user/login')
def citizen_data_to_csv(request):
    # Convert the contacts to a csv file. Filter the non synced contacts Save the csv. 
    # Redirect to google contacts import page
    response = HttpResponse(content_type = 'text/csv')
    fields = ['Name','Given Name','Additional Name','Family Name','Yomi Name','Given Name Yomi',
            'Additional Name Yomi','Family Name Yomi','Name Prefix','Name Suffix','Initials',
             'Nickname','Short Name','Maiden Name','Birthday','Gender','Location','Billing Information',
            'Directory Server','Mileage','Occupation','Hobby','Sensitivity','Language','Photo','Group Membership',
            'Phone 1 - Type','Phone 1 - Value'
        ]
        
    response['Content-Disposition'] = f'attachment; filename=Contacts_{timezone.now()}.csv'
    
    csv_file= csv.DictWriter(response, fieldnames=fields)
    csv_file.writeheader()
    for citizen in Citizen.objects.filter(uploaded_to_google=False):
        # Get the groups and padd with double colon
        groups = ' ::: '.join([gp.name for gp in citizen.group_set.all()])
        #"Women ::: Farmer ::: * coworkers ::: * friends ::: * myContacts"
        csv_file.writerow(
                {'Name':citizen.first_name,'Given Name':citizen.last_name,'Additional Name':'','Family Name':citizen.surname,'Yomi Name':'',
                'Given Name Yomi':'','Additional Name Yomi':'', 'Family Name Yomi':'', 'Name Prefix':'', 'Name Suffix':'', 'Initials':'',
                'Nickname':'', 'Short Name':'', 'Maiden Name':'', 'Birthday':citizen.dob, 'Gender':citizen.get_gender_display(), 'Location':citizen.location,
                'Billing Information':'','Directory Server':'', 'Mileage':'', 'Occupation':'', 'Hobby':'', 'Sensitivity':'', 'Language':'', 'Photo':'', 
                'Group Membership':groups,'Phone 1 - Type':'Mobile', 'Phone 1 - Value':f"+254 {int(citizen.phone_number)}"
                }
            )

        #Update the uploaded to google account 
        citizen.uploaded_to_google = True
        citizen.save()

    return response


@login_required(login_url='/user/login')
def statistics(request):
    citizen_count = Citizen.objects.all().count()
    group_count = Group.objects.all().count()
    messages = Messages.objects.values('is_sorted').annotate(isSorted = Count('is_sorted'))
    issorted = [p.get('isSorted') for p in messages]

    return render(request,'statistics.html', {'citizen':citizen_count,'group':group_count,'mymessages':issorted})


@login_required(login_url='/user/login')
def data_analysis(request):
    citizen = serialize('json', Citizen.objects.all())
    groups = serialize('json',Group.objects.all())
    mymessages = serialize('json', Messages.objects.all())
    return HttpResponse(json.dumps({'citizen':citizen,'groups':groups,'messages':mymessages}))


@login_required(login_url='/user/login')
def about(request):
    return render(request,'googled764035286992e26.html')


@login_required(login_url='/user/login')
def add_to_group(request):
    if request.method == 'POST':
        data = request.POST.copy()
        user = get_object_or_404(Citizen, pk = data.get('user'))
        
        for group in data.getlist('groups'):
            currentgroup = Group.objects.get(name = group)
            currentgroup.members.add(user)
            currentgroup.save()
        return HttpResponseRedirect(f'/citizen/{user.id_number}')
    else:
        return redirect('/manycitizen/')

# Formsets

# TODO
#  REMOVE DEGUG = TRUE
#  TEST THE APP WITH THE CLIENT
# 
# =================== GROUPS VIEWS =========================
#Events 
class EventsCreateView(LoginRequiredMixin,CreateView):
    model = Events
    template_name = "createupdate.html"
    fields = "__all__"
    extra_context = {'title':'Create Event'}

class EventsUpdateView(LoginRequiredMixin,UpdateView):
    model = Events
    template_name = "createupdate.html"
    fields = "__all__"
    extra_context = {'title': 'Update Event'}

#Bursary
class BursaryListView(LoginRequiredMixin,ListView):
    model = Bursary
    template_name = "bursary/bursarylist.html"
    context_object_name = 'bursaries'
    paginate_by = 25
    order_by = 'dat'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != '' and query != None:
            try:
                if(isinstance(int(query), int)):
                    queryset = Bursary.objects.filter(
                                        Q(parent=Citizen.objects.filter(id_number=query)[:1])|
                                        Q(student = Student.objects.filter(admission_number = query)[:1])    
                                )
                    return queryset
            except ValueError:
                queryset = Bursary.objects.filter(student = Student.objects.filter(school__icontains=query)[:1])
                return queryset
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = Bursary.objects.all().aggregate(Sum('amount_awarded'))
        print( Bursary.objects.all().aggregate(Sum('amount_awarded')) )
        context['yearly_budget'] = Bursary.objects.values('amount_awarded', 'date_issued').annotate(Total=Sum('amount_awarded'))
        return context
    
    
class BursaryCreateView(LoginRequiredMixin, CreateView):
    model = Bursary
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title': 'Create Bursary'}

class BursaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Bursary
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title': 'Update Bursary'}

# NHIF
class NhifListView(LoginRequiredMixin, ListView):
    model = Nhif
    template_name = 'nhiflist.html'
    context_object_name = 'nhifs'

class NhifCreateView(LoginRequiredMixin, CreateView):
    model = Nhif
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title':'Add NHIF Details'}

class NhifUpdateView(LoginRequiredMixin,UpdateView):
    model = Nhif
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title':'Update NHIF Details'}

# NCA
class NCAListView(LoginRequiredMixin,ListView):
    model = NCA
    template_name = 'ncalist.html'
    context_object_name = 'ncas'

class NCACreateView(LoginRequiredMixin,CreateView):
    model = NCA
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title': 'Add NCA Details'}

class NCAUpdateView(LoginRequiredMixin, UpdateView):
    model = NCA
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title': 'Update NCA Details'}

# Self Help Group
class SelfHelpGroupListView(LoginRequiredMixin,ListView):
    model = SelfHelpGroup
    template_name = 'selfgroup.html'
    context_object_name = 'selfgroups'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query != '' and query !=None:
            return SelfHelpGroup.objects.filter(name__icontains = query)
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class SelfHelpGroupCreateView(LoginRequiredMixin,CreateView):
    model = SelfHelpGroup
    template_name = 'createupdate.html'
    extra_context = {'title':'Create Self Help Group'}
    fields = "__all__"

class SelfHelpGroupUpdateView(LoginRequiredMixin,UpdateView):
    model = SelfHelpGroup
    template_name = 'createupdate.html'
    extra_context = {'title':'Update Self Help Group'}
    fields = "__all__"


# College
class CollegeListView(LoginRequiredMixin,ListView):
    model = College
    template_name = 'collegelist.html'
    context_object_name = 'colleges'
    paginate_by = 25

    def get_queryset(self):
        query_name = self.request.GET.get('q')
        if query_name != None and query_name != '':
            return College.objects.filter(citizen=query_name)
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CollegeCreateView(LoginRequiredMixin,CreateView):
    model = College
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title':'Create College'}

class CollegeDetailView(LoginRequiredMixin,DetailView):
    model = College

class CollegeUpdateView(LoginRequiredMixin, UpdateView):
    model = College
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title':'Update College'}


# Student Sponsored
def createStudent(request):
    if request.method == "POST":
        data = request.POST.copy()
        for key in ['surname', 'first_name','last_name','gender','dob']:
            del data[key]

        print(data)
        admission_number = data.get('admission_number')
        form = StudentForm(request.POST)
        if form.is_valid():
            person = create_person(request.POST)
            student = form.save(commit=False)
            student.person = person
            student.save()
            return HttpResponseRedirect(f'/student/')
    else:
        form = StudentForm()
        person = PersonForm()
    return render(request,"students/studentcreate.html",{'form':form,'person':person,'title':'Add Student'})

class StudentListView(LoginRequiredMixin,ListView):
    model = Student
    template_name = 'students/studentlist.html'
    context_object_name = 'students'
    paginate_by = 25
    ordering = "admission_number"

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q')
        if  query != '' and query != None:
            # Check if the value id an integer |
            try:
                if isinstance(int(query), int):
                    queryset = Student.objects.filter(Q(admission_number=query))
                    return queryset
            except ValueError:
                queryset = Student.objects.filter(
                    Q(school__icontains=query)|
                    Q(person=Person.objects.filter(first_name__startswith=query)[:1])|
                    Q(person=Person.objects.filter(
                        last_name__startswith=query)[:1])
                )              

                return queryset
        return super().get_queryset()

class StudentDetailView(LoginRequiredMixin,DetailView):
    model = Student
    template_name = "students/studentdetail.html" 
    context_object_name = "student"

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = Results.objects.filter(student = self.kwargs['pk'])
        return context

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title':'Create Student'}


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = 'createupdate.html'
    fields = '__all__'
    extra_context = {'title':'Update Student'}

# Team Members
class TeamMembersListView(LoginRequiredMixin,ListView):
    model = TeamMembers
    context_object_name = 'teams'
    template_name = "teamlist.html"

class TeamMembersCreateView(LoginRequiredMixin,CreateView):
    model = TeamMembers
    template_name = "createupdate.html"
    fields = "__all__"
    extra_context = {'title':'Create Team Member'}


class TeamMembersUpdateView(LoginRequiredMixin, UpdateView):
    model = TeamMembers
    template_name = "createupdate.html"
    fields = "__all__"
    extra_context = {'title': 'Update Team Member'}

# Curriculum Vitae
class CurriculumListView(LoginRequiredMixin,ListView):
    model = CuriculumVitae
    template_name = "cvlist.html"
    context_object_name = 'cvs'


class CurriculumCreateView(LoginRequiredMixin,CreateView):
    model = CuriculumVitae
    template_name = "createupdate.html"
    fields = "__all__"
    extra_context = {"title":'Add to CVs'}


class CurriculumUpdateView(LoginRequiredMixin, UpdateView):
    model = CuriculumVitae
    template_name = "createupdate.html"
    fields = "__all__"
    extra_context = {"title": 'Add to CVs'}

# Projects: CRUD
class ProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/projectlist.html'
    context_object_name = 'projects'

class ProjectsCreateView(LoginRequiredMixin,CreateView):
    model = Project
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title':'Create Project'}


class ProjectsUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'createupdate.html'
    fields = "__all__"
    extra_context = {'title': 'Create Project'}

from django.utils.timezone import make_aware
import datetime
def createReports(request):
    # Get the current week, initialize a start anad end dates of the week
    date = timezone.now()
    start_date = timezone.now() - timedelta(days = date.isoweekday())
    end_date = start_date + timedelta(days=5)
    if request.GET.get('start_date') != None and request.GET.get('end_date') != None:
        start_date = make_aware(
            datetime.datetime.strptime(
                request.GET.get('start_date'),
                '%Y-%m-%d'
                )
            )
        end_date = make_aware(
            datetime.datetime.strptime(
                request.GET.get('end_date'),
                '%Y-%m-%d'
                )
            )

        print(start_date, end_date)
        citizen =  Messages.objects.filter(Q(date_created__lte = end_date),Q(date_created__gte = start_date))
    else:
        future_date = date + timedelta(days=5)
        citizen = citizen = Messages.objects.filter(
            Q(date_created__lte=end_date), Q(date_created__gte=start_date))
    return render(request,'report.html',{'weekreport':citizen,'start_date':start_date,'end_date':end_date})

# class ReportView(TemplateView):
#     template_name = "report.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context[""] = 
#         return context
    
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
    
#     def get
    
    
    
# TODO :
# Customize the CRUD to models related to person and citizen
# Customize the detail views: section view and such
# 
