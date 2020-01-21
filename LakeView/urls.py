from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sms/', include('sms.urls')),
    path('user/', include('user.urls')),
    path('',include('citizens.urls'))
]

# admin.site