from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Event, Gallery, Registration, Message, Sponsor, NewsPost
from .forms import RegistrationForm, ContactForm


def _latest_event():
    try:
        return Event.objects.latest("date")
    except Event.DoesNotExist:
        return None


def index(request):
    context = {
        "event": _latest_event(),
        "sponsors": Sponsor.objects.filter(active=True),
    }
    return render(request, "index.html", context)


def gallery(request):
    galleries = Gallery.objects.filter(published=True)

    context = {
        "galleries": galleries,
    }
    return render(request, "gallery.html", context)


def about(request):
    context = {
        "event": _latest_event(),
    }
    return render(request, "about.html", context)


def evolution(request):
    return redirect("core:about")


def registration(request):
    event = _latest_event()

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
    event = _latest_event()

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


def sponsorship(request):
    context = {
        "event": _latest_event(),
        "sponsors": Sponsor.objects.filter(active=True),
    }
    return render(request, "sponsorship.html", context)


def news_list(request):
    context = {
        "event": _latest_event(),
        "posts": NewsPost.objects.filter(published=True),
    }
    return render(request, "news_list.html", context)


def news_detail(request, slug):
    post = get_object_or_404(NewsPost, slug=slug, published=True)
    context = {
        "event": _latest_event(),
        "post": post,
        "posts": NewsPost.objects.filter(published=True).exclude(pk=post.pk)[:3],
    }
    return render(request, "news_detail.html", context)
