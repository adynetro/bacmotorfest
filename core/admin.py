from django.contrib import admin
from .models import Event, Gallery, GalleryImage, Registration, Message


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


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["title", "year", "published", "image_count"]
    list_filter = ["year", "published"]
    list_editable = ["published"]
    inlines = [GalleryImageInline]
    ordering = ["-year"]

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
