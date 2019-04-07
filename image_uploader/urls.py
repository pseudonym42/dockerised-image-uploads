from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken import views


urlpatterns = [
    path('', admin.site.urls),
    path('api/', include('images.urls')),
    path('api_token', views.obtain_auth_token, name="token")
]
