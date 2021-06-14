#from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from .models import City, Country, Owner, Property, PropertyImage, PropertyTrace, State
from .serializers import CitySerializer, CountrySerializer, OwnerSerializer, PropertyImageSerializer, PropertySerializer, PropertyTraceSerializer, StateSerializer
#, UserSerializer

# Create your views here.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminUser]

#the endpoints are enabled by user, some read-only for anonymous, and some for authenticaded users
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticated]

class PropertyTraceViewSet(viewsets.ModelViewSet):
    queryset = PropertyTrace.objects.all()
    serializer_class = PropertyTraceSerializer
    permission_classes = [IsAuthenticated]