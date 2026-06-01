from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("gallery/", views.gallery, name="gallery"),
    path("registration/", views.registration, name="registration"),
    path("contact/", views.contact, name="contact"),
]
