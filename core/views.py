from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, Gallery, Registration, Message
from .forms import RegistrationForm, ContactForm


def index(request):
    try:
        event = Event.objects.latest("date")
    except Event.DoesNotExist:
        event = None

    context = {
        "event": event,
    }
    return render(request, "index.html", context)


def gallery(request):
    galleries = Gallery.objects.filter(published=True)

    context = {
        "galleries": galleries,
    }
    return render(request, "gallery.html", context)


def registration(request):
    try:
        event = Event.objects.latest("date")
    except Event.DoesNotExist:
        event = None

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration submitted successfully! We will confirm your registration shortly.")
            return redirect("core:registration")
    else:
        form = RegistrationForm()

    context = {
        "form": form,
        "event": event,
    }
    return render(request, "registration.html", context)


def contact(request):
    try:
        event = Event.objects.latest("date")
    except Event.DoesNotExist:
        event = None

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully. We will get back to you soon!")
            return redirect("core:contact")
    else:
        form = ContactForm()

    context = {
        "form": form,
        "event": event,
    }
    return render(request, "contact.html", context)
