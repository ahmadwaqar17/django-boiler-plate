from django.urls import path, include

# Register all your API v1 endpoints here
urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('patients/', include('apps.patients.urls')),
    path('studies/', include('apps.studies.urls')),
]
