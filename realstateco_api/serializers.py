import datetime
from .models import City, Owner, Property, PropertyImage, PropertyTrace, State, Country
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "username")

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.HyperlinkedModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    state_id = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())

    class Meta:
        model = City
        #fields = '__all__'
        fields = ("uuid", "name", "country_id", "state_id")
    
        #override the method for including the country and state objects
    def create(self, validated_data):
        country = validated_data.pop('country_id')
        state = validated_data.pop('state_id')
        owner = City.objects.create(country=country, state=state, **validated_data)
        return owner

class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Owner
        fields = ("uuid", "address", "photo", "birthday", "user_id")
    
    def validate_birthday(self, value):
        if value > datetime.today() - datetime.timedelta(days=(365 * 18)):
            serializers.ValidationError("The owner must be an adult")
        else:
            return value

        #override the method for including the user object
    def create(self, validated_data):
        user = validated_data.pop('user_id')
        owner = Owner.objects.create(user=user, **validated_data)
        return owner

class PropertySerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(queryset=Owner.objects.all())
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Property
        fields = ("uuid", "name", "address", "price", "year", "owner_id", "city_id")

        #override the method for including the owner and city objects
    def create(self, validated_data):
        owner = validated_data.pop('owner_id')
        city = validated_data.pop('city_id')
        property = Property.objects.create(owner=owner, city=city, **validated_data)
        return property

class PropertyImageSerializer(serializers.HyperlinkedModelSerializer):
    property_id = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())

    class Meta:
        model = PropertyImage
        fields = ("uuid", "file", "enabled", "property_id")

        #override the method for including the property object
    def create(self, validated_data):
        property = validated_data.pop('property_id')
        property_image = PropertyImage.objects.create(property=property, **validated_data)
        return property_image

class PropertyTraceSerializer(serializers.HyperlinkedModelSerializer):
    property_id = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())

    class Meta:
        model = PropertyTrace
        fields = ("uuid", "name", "price", "tax", "sold_on", "property_id")

        #override the method for including the property object
    def create(self, validated_data):
        property = validated_data.pop('property_id')
        property_trace = PropertyTrace.objects.create(property=property, **validated_data)
        return property_trace