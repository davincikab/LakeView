from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('',include('citizens.urls'))
]

# admin.site
admin.site.site_header = "Lakeview Ward Admin"
admin.site.site_title = "Lakeview Ward Portal"
admin.site.index_title = "Welcome to Lakeview Ward Portal"

