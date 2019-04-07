from django.contrib import admin
from django.urls import path, include

from rest_framework.authtoken import views

from images.api_views import(
    ImageList,
    ImageCreate,
    ImageGet
)


urlpatterns = [
    path('images/list', ImageList.as_view()),
    path('images/create', ImageCreate.as_view()),
    path('images/get/<int:pk>', ImageGet.as_view())
]

