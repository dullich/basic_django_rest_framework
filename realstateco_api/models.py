from django.contrib import admin
from uuid import uuid4
# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import RESTRICT
from django.db.models.fields import UUIDField
from django.utils import tree

#This model is useful when another model needs tracking about creation or modification
#Those models will inherit from this
class Timestamped(models.Model):
    created_on=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(null=True, blank=True)
    created_by=models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="+",
        null=True,
        blank=True,
    )
    modified_by=models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="+",
        null=True,
        blank=True,
    )
    created_from_ip=models.GenericIPAddressField(blank=True, null=True)
    modified_from_ip=models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        abstract=True
        get_latest_by = 'created_on'
        ordering = ['-created_on', '-modified_on']

class Country(models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name=models.CharField(max_length=50, unique=True)
    iso2=models.CharField(max_length=2)
    iso3=models.CharField(max_length=3)

    REQUIRED_FIELDS=["name", "iso2", "iso3"]
    #field_order = ["uuid", "name", "iso2", "iso3"]
    
    def __str__(self):
        return self.name

class State(models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name=models.CharField(max_length=50, unique=True)
    
    REQUIRED_FIELDS=["name"]
    #field_order = ["uuid", "name"]


    def __str__(self):
        return self.name

class City(models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name=models.CharField(max_length=50)
    state=models.ForeignKey(
        State,
        on_delete=models.RESTRICT,
        related_name="cities",
    )
    country=models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        related_name="cities",
    )

    REQUIRED_FIELDS=["name", "state", "country"]
    #field_order = ["uuid", "name", "state", "country"]
    
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "state", "country")

class Owner(Timestamped, models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    address=models.CharField(max_length=100)
    photo=models.URLField(blank=True, null=True)
    birthday=models.DateField()
    user=models.OneToOneField(
        User,
        on_delete=RESTRICT,
        related_name="owner",
    )

    REQUIRED_FIELDS=["address", "birthday", "user"]
    #field_order = ["uuid", "address", "photo", "birthday", "user"]
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Property(Timestamped, models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner=models.ForeignKey(
        Owner,
        on_delete=models.RESTRICT,
        related_name="properties",
    )
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    city=models.ForeignKey(
        City,
        on_delete=models.RESTRICT,
        related_name="properties",
    )
    price=models.FloatField()
    code_internal=models.CharField(max_length=100)
    year=models.IntegerField()

    REQUIRED_FIELDS=["name", "address", "city", "price", "year"]
    #field_order = ["uuid", "address", "city", "price", "code_internal", "year"]

    def __str__(self):
        return self.name + " " + self.address
    
class PropertyImage(Timestamped, models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    property=models.ForeignKey(
        Property,
        on_delete=models.RESTRICT,
        related_name="property_images",
    )
    file=models.URLField()
    enabled=models.BooleanField(default=True)

    REQUIRED_FIELDS=["property", "file"]
    #field_order = ["uuid", "property", "file", "enabled"]

class PropertyTrace(Timestamped, models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid4, editable=False)
    property=models.ForeignKey(
        Property,
        on_delete=models.RESTRICT,
        related_name="property_traces",
    )
    name=models.CharField(max_length=50)
    price=models.FloatField()
    tax=models.FloatField()
    sold_on=models.DateTimeField()

    REQUIRED_FIELDS=["property", "name", "price", "tax"]
    #field_order = ["uuid", "property", "name", "price", "tax", "sold_on"]
