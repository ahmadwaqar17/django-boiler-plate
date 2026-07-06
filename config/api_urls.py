from django.urls import include, path

# Register all your API v1 endpoints here
urlpatterns = [
    path("users/", include("apps.users.urls")),
    # path('another_app/', include('apps.another_app.urls')),
]
