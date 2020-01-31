from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='citizen-home'),
    path('manycitizen/',CitizenListView.as_view(), name="list-view"),
    path('citizen/<int:pk>/', CitizenDetailView.as_view(),name="citizen-detail"),
    path('citizen/update/<int:pk>/', CitizenUpdateView.as_view(), name="citizen-update"),
    path('citizen/delete/<int:pk>/', CitizenDeleteView.as_view(), name="citizen-delete"),
    path('citizen/create/', create_citizen, name="citizen-create"),
    # Messages

    path('citizen/<id_number>/message/create/', MessagesCreateView.as_view(), name="message-create"),
    path('citizen/<id_number>/message/<int:pk>/update/',MessagesUpdateView.as_view(), name="message-update"),
    
    # Groups
    path('group/',GroupListView.as_view(), name="group-list"),
    path('group/<int:pk>/', GroupDetailView.as_view(), name="group-detail"),
    path('group/delete/<int:pk>/',GroupDeleteView.as_view(), name="group-delete"),
    path('group/create/', GroupCreateView.as_view(), name="group-create"),
    path('group/update/<int:pk>/', GroupUpdateView.as_view(),name='group-update'),

    # GroupEvents
    path('group_events/create/', GroupEventsCreateView.as_view(), name="group-event-create"),
    path('group_events/update/<int:pk>/', GroupEventsUpdateView.as_view(), name="group-event-update"),
    path('group_events/delete/<int:pk>/', GroupEventsDeleteView.as_view(), name="group-event-delete"),

    #Events
    path('event/create/',EventsCreateView.as_view(),name="event-create"),
    path('event/update/<int:pk>/',EventsUpdateView.as_view(),name="event-update"),

    #Bursary
    path('bursary/', BursaryListView.as_view(), name="bursary-list"),
    path('bursary/create/',BursaryCreateView.as_view(),name="bursary-create"),
    path('bursary/update/<int:pk>/',BursaryUpdateView.as_view(),name="bursary-update"),

    # Projects 
    path('projects/', ProjectsListView.as_view(), name="project-list"),
    path('projects/create/', ProjectsCreateView.as_view(), name="project-create"),
    path('projects/update/<int:pk>/', ProjectsUpdateView.as_view(), name="project-update"),

    # Self Help Group
    path('selfhelpgroup/', SelfHelpGroupListView.as_view(), name="selfgroup"),
    path('selfhelpgroup/create/', SelfHelpGroupCreateView.as_view(), name="selfgroup-create"),
    path('selfhelpgroup/update/<int:pk>/', SelfHelpGroupUpdateView.as_view(), name="selfgroup-update"),

    # Students
    path('student/', StudentListView.as_view(), name="list-student"),
    path('student/detail/<int:pk>/',StudentDetailView.as_view(),name="student-detail"),
    path('student/create/', createStudent, name="create-student"),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name="update-student"),

    # NHIF
    path('nca/list/',NCAListView.as_view(),name = "nca-list"),
    path('nca/create/',NCACreateView.as_view(),name = "nca-create"),
    path('nca/update/<int:pk/',NCAUpdateView.as_view(),name = "nca-update"),

    # NHIF
    path('nhif/', NhifListView.as_view(),name = "nhif-list"),
    path('nhif/create/',NhifCreateView.as_view(), name="nhif-create"),
    path('nhif/update/<int:pk>/',NhifUpdateView.as_view(), name="nhif-update"),

    # Team Members
    path('teammembers/', TeamMembersListView.as_view(), name="team-list"),
    path('teammembers/create/', TeamMembersCreateView.as_view(), name="team-create"),
    path('teammembers/update/<int:pk>/',TeamMembersUpdateView.as_view(), name="team-update"),

    # CV
    path('cv/',CurriculumListView.as_view(),name="cv-list"),
    path('cv/create/',CurriculumCreateView.as_view(), name ="cv-create"),
    path('cv/update/<int:pk>/',CurriculumUpdateView.as_view(),name="cv-update"),

    #College
    path('college/', CollegeListView.as_view(), name="college-list"),
    path('college/create/', CollegeCreateView.as_view(), name="college-create"),
    path('college/update/<int:pk>/',CollegeUpdateView.as_view(), name="college-update"),

    # Others
    path('addtogroup/',add_to_group,name="add-group"),
    path('statistic/',statistics, name="stats"),
    path('data/', data_analysis, name="data"),
    path('report/',createReports, name='reports'),

    # Export Contacts
    path('citizencontacts/', citizen_data_to_csv, name="downup")
]

# admin.site

urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



