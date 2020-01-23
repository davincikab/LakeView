from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter 
from .apiviews import *

router = DefaultRouter()
router.register('citizens', CitizenViewSet, 'citizens')
router.register('messages', MessageViewSet, 'message')
router.register('groups', GroupViewSet, 'group')

urlpatterns = [
    path('', home, name='citizen-home'),
    path('manycitizen/',CitizenListView.as_view(), name="list-view"),
    path('citizen/<int:pk>/', CitizenDetailView.as_view(),name="citizen-detail"),
    path('citizen/update/<int:pk>/', CitizenUpdateView.as_view(), name="citizen-update"),
    path('citizen/delete/<int:pk>/', CitizenDeleteView.as_view(), name="citizen-delete"),
    path('citizen/create/', CitizenCreateView.as_view(), name="citizen-create"),
    # Messages

    path('citizen/<id_number>/message/create/', MessagesCreateView.as_view(), name="message-create"),
    path('citizen/<id_number>/message/<int:pk>/update/',MessagesUpdateView.as_view(), name="message-update"),
    
    # Groups
    path('group/',GroupListView.as_view(), name="group-list"),
    path('group/<int:pk>/', GroupDetailView.as_view(), name="group-detail"),
    path('group/delete/<int:pk>/',GroupDeleteView.as_view(), name="group-delete"),
    path('group/create/', GroupCreateView.as_view(), name="group-create"),
    path('group/update/<int:pk>/', GroupUpdateView.as_view(),name='group-update'),

    # Others
    path('addtogroup/',add_to_group,name="add-group"),
    path('statistic/',statistics, name="stats"),
    path('data/', data_analysis, name="data"),

    # Contacts
    path('googled764035286992e26.html', about, name='about', ),
    path('contacts/', test_contacts_api,name='contacts'),
    path('authorize/', authorize, name= 'authorize'),
    path('oauth2callback/', oauth2callback, name='oauth2callback'),

    # 
    path('citizencontacts/', citizen_data_to_csv, name="downup")
]

# urlpatterns+=router.urls
# admin.site

urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



