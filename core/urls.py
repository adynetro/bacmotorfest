from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("evolution/", views.evolution, name="evolution"),
    path("sponsorship/", views.sponsorship, name="sponsorship"),
    path("news/", views.news_list, name="news_list"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("gallery/", views.gallery, name="gallery"),
    path("registration/", views.registration, name="registration"),
    path("contact/", views.contact, name="contact"),
]
