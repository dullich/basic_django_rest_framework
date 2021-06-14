from django.contrib import admin
from django.contrib.auth.models import User
from .models import City, Property, PropertyImage, PropertyTrace, State, Country, Owner
import datetime

# Register your models here.
# To avoid writing in each view the code for complete the tracking information.
# The Timestamped Admin View is created and each view that needs timestamp will inherit from this
class TimestampedAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Control information", {
            "classes": ("collapse",),
            "fields": ("created_by", "created_from_ip", "modified_on", "modified_by", "modified_from_ip"),
        }),
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by=request.user
            obj.created_from_ip=request.META.get("REMOTE_ADDR")
        if change:
            obj.modified_on=datetime.datetime.now()
            obj.modified_by=request.user
            obj.modified_from_ip=request.META.get("REMOTE_ADDR")
        super().save_model(request, obj, form, change)

class UserAdmin(TimestampedAdmin):
    model:User

    fieldsets = [
        (None, {
            "fields": ("address", "birthday", "user"),
        }),
    ]
    fieldsets.append(TimestampedAdmin.fieldsets[0])

class OwnerAdmin(TimestampedAdmin):
    model:Owner

    fieldsets = [
        (None, {
            "fields": ("address", "birthday", "user"),
        }),
    ]
    fieldsets.append(TimestampedAdmin.fieldsets[0])


class PropertyAdmin(TimestampedAdmin):
    model:Property

    fieldsets = [
        (None, {
            "fields": ("name", "address", "city", "price", "code_internal", "year"),
        }),
    ]
    fieldsets.append(TimestampedAdmin.fieldsets[0])

class PropertyImageAdmin(TimestampedAdmin):
    model:PropertyImage

    fieldsets = [
        (None, {
            "fields": ("property", "file", "enabled"),
        }),
    ]
    fieldsets.append(TimestampedAdmin.fieldsets[0])

class PropertyTraceAdmin(TimestampedAdmin):
    model:PropertyTrace

    fieldsets = [
        (None, {
            "fields": ("property", "name", "price", "tax", "sold_on"),
        }),
    ]
    fieldsets.append(TimestampedAdmin.fieldsets[0])

#Models are added to admin site for management
admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(PropertyTrace, PropertyTraceAdmin)