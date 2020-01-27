from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse, resolve

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.conf import settings
from django.utils import timezone
from django.core.serializers import serialize
from django.db.models import Count

from .models import Citizen, Messages, Group, GroupEvents

import os
import csv
import json

@login_required(login_url='/user/login')
def home(request):
    context = {'data':'HOME IS WHERE MY HEART IS'}
    return render(request,'index.html', context)


class CitizenListView(LoginRequiredMixin, ListView):
    model = Citizen
    context_object_name = 'citizens'
    template_name  = 'citizen/citizenlist.html'
    paginate_by = 7

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
        return context
    
    def get_queryset(self):
        return super().get_queryset()


class CitizenCreateView(LoginRequiredMixin, CreateView):
    model = Citizen
    context_object_name = "citizen"
    template_name = "citizen/citizenupdate.html"
    fields = "__all__"

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
            return self.form_valid(form,user)
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
