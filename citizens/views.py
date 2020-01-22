from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Citizen, Messages, Group
from django.urls import reverse_lazy, reverse, resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
import os
from django.core.serializers import serialize

@login_required(login_url='/user/login')
def home(request):
    context = {'data':'HOME IS WHERE MY HEART IS'}
    return render(request,'index.html', context)


class CitizenListView(ListView):
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
    

class CitizenDetailView(DetailView,LoginRequiredMixin):
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


class CitizenCreateView(CreateView,LoginRequiredMixin):
    model = Citizen
    context_object_name = "citizen"
    template_name = "citizen/citizenupdate.html"
    fields = "__all__"

class CitizenUpdateView(UpdateView,LoginRequiredMixin):
    model = Citizen
    context_object_name = 'citizen'
    template_name = "citizen/citizenupdate.html"
    fields = "__all__"


class CitizenDeleteView(DeleteView,LoginRequiredMixin):
    model = Citizen
    template_name = "citizen/citizendelete.html"
    success_url = reverse_lazy("list-view")


class MessagesCreateView(CreateView,LoginRequiredMixin):
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



class MessagesUpdateView(UpdateView, LoginRequiredMixin):
    model = Messages
    template_name = "message/messagecreate.html"
    fields = "__all__"

class GroupListView(ListView,LoginRequiredMixin):
    model = Group
    context_object_name = "groups"
    template_name = 'groups/group_list.html'

    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        return context


class GroupDetailView(DetailView,LoginRequiredMixin):
    model = Group
    context_object_name = "group"
    template_name = 'groups/group_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        return super().get_queryset()

class GroupUpdateView(UpdateView,LoginRequiredMixin):
    model = Group
    template_name = "groups/group_update.html"
    fields = "__all__"

class GroupCreateView(CreateView,LoginRequiredMixin):
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

class GroupDeleteView(DeleteView,LoginRequiredMixin):
    model = Group
    template_name = "groups/group_delete.html"
    success_url = reverse_lazy("group-list")


def searchCitizen(id=None):
    if id == '' or id == None:
        results = Citizen.objects.all()
    else:
        results = Citizen.objects.filter(pk=id)
    return results

# Using F() for better queries
class sendMessage:
    def sendToGroup(self):
        pass

    def sendToIndividual(self):
        pass
    
def statistics(request):
    context = {'citizen': serialize('json', Citizen.objects.all())}
    context['groups'] = serialize('json',Group.objects.all())
    return render(request,'statistics.html', context)

def about(request):
    return render(request,'googled764035286992e26.html')

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


# Register user, add messages, add to group
#  Use a modal to handle add to group and messages
# Formsets

            # Batch a processing
            # send POT REQEUST TO https://www.google.com/m8/feeds/groups/{userEmail}/full/batch
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENTS_SECRETS_FILE = staticfiles_storage.path("client_secret.json")
SCOPES = ['https://www.google.com/m8/feeds/']

API_SERVICE_NAME = 'contacts'
API_VERSION = 'v3'

def test_contacts_api(request):
    # Client and scopes
    if 'credentials' not in request.session:
        return redirect('authorize')
    
    credentials = goole.oauth2.credentials.Credentials(
        **request.session['credentials']
    )

    feeds = googleapiclient.discovery.build(
        API_SERVICE_NAME,API_VERSION,credentials=credentials
    )

    contacts = feeds

    request.session['credentials'] = credentials_to_dict(credentials)
    return HttpResponse(contacts)

def authorize(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENTS_SECRETS_FILE,
        SCOPES
    )

    flow.redirect_uri = 'http://127.0.0.1:8000/contacts/'
    authorization_url, state = flow.authorization_url(
        access_type = 'offline',
        login_hint = 'davidnganganjeri079@gmail.com',
        include_granted_scopes = 'true'
    )

    request.session['state'] = state

    print(authorization_url)
    return redirect(authorization_url)

def oauth2callback(request):
    state = request.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENTS_SECRETS_FILE,scopes=SCOPES,state=state
    )

    flow.redirect_uri = 'http://127.0.0.1:8000/contacts/'  # Callback url similar to
    authorization_response = 'http://127.0.0.1:8000/oauth2callback/'  # Request url
    flow.fetch_token (authorization_response = authorization_response)
    credentials = flow.credentials
    request.session ['credentials'] = credentials_to_dict(credentials)

    return redirect('contacts')

def revoke(request):
    pass

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

def clear_credentials(request):
    pass
