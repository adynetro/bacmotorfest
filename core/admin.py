from pathlib import Path

from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse
from .models import Event, Gallery, GalleryImage, Registration, Message, Sponsor


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "location", "registration_open"]
    list_editable = ["registration_open"]
    fieldsets = (
        ("Event Information", {
            "fields": ("title", "description", "date", "location")
        }),
        ("Contact", {
            "fields": ("contact_email", "contact_phone")
        }),
        ("Settings", {
            "fields": ("registration_open",)
        }),
    )


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ["image", "caption", "order"]


class GalleryBulkUploadForm(forms.Form):
    class MultipleFileInput(forms.ClearableFileInput):
        allow_multiple_selected = True

    class MultipleFileField(forms.FileField):
        def clean(self, data, initial=None):
            single_file_clean = super().clean
            if isinstance(data, (list, tuple)):
                result = []
                for uploaded_file in data:
                    result.append(single_file_clean(uploaded_file, initial))
                return result
            if data:
                return [single_file_clean(data, initial)]
            return []

    images = MultipleFileField(
        widget=MultipleFileInput(),
        required=False,
        help_text="Select one or multiple images.",
    )
    start_order = forms.IntegerField(
        required=False,
        min_value=0,
        help_text="Optional. Leave empty to continue from current max order.",
    )
    use_filename_as_caption = forms.BooleanField(
        required=False,
        initial=True,
        help_text="Use each file name as image caption.",
    )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["title", "year", "published", "image_count"]
    list_filter = ["year", "published"]
    list_editable = ["published"]
    inlines = [GalleryImageInline]
    ordering = ["-year"]
    change_form_template = "admin/core/gallery/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/bulk-upload/",
                self.admin_site.admin_view(self.bulk_upload_view),
                name="core_gallery_bulk_upload",
            ),
        ]
        return custom_urls + urls

    def bulk_upload_view(self, request, object_id):
        gallery = get_object_or_404(Gallery, pk=object_id)

        if request.method == "POST":
            form = GalleryBulkUploadForm(request.POST, request.FILES)
            files = form.files.getlist("images")

            if form.is_valid() and files:
                max_order = gallery.images.order_by("-order").values_list("order", flat=True).first()
                order = form.cleaned_data["start_order"]
                if order is None:
                    order = (max_order + 1) if max_order is not None else 0

                use_filename_as_caption = form.cleaned_data["use_filename_as_caption"]
                created_count = 0

                for image_file in files:
                    caption = ""
                    if use_filename_as_caption:
                        caption = Path(image_file.name).stem.replace("_", " ").replace("-", " ").strip()

                    GalleryImage.objects.create(
                        gallery=gallery,
                        image=image_file,
                        caption=caption,
                        order=order,
                    )
                    order += 1
                    created_count += 1

                self.message_user(
                    request,
                    f"Uploaded {created_count} image(s) to {gallery.title}.",
                    level=messages.SUCCESS,
                )
                return HttpResponseRedirect(
                    reverse("admin:core_gallery_change", args=[gallery.pk])
                )
            elif not files:
                form.add_error("images", "Please select at least one image.")
        else:
            form = GalleryBulkUploadForm()

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "gallery": gallery,
            "form": form,
            "title": f"Bulk upload images: {gallery.title}",
        }
        return render(request, "admin/core/gallery/bulk_upload.html", context)

    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = "Images"


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "status", "created_at"]
    list_filter = ["status", "created_at"]
    list_editable = ["status"]
    search_fields = ["name", "email", "phone"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Personal Information", {
            "fields": ("name", "email", "phone")
        }),
        ("Bike Information", {
            "fields": ("bike_info",)
        }),
        ("Status", {
            "fields": ("status",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "read", "created_at"]
    list_filter = ["read", "created_at"]
    list_editable = ["read"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["created_at"]
    fieldsets = (
        ("Message Information", {
            "fields": ("name", "email", "subject", "message")
        }),
        ("Status", {
            "fields": ("read",)
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ["name", "order", "active"]
    list_editable = ["order", "active"]
    list_filter = ["active"]
    search_fields = ["name", "benefits", "website"]
    ordering = ["order", "name"]
