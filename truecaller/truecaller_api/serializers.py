from rest_framework import serializers
from rest_framework.serializers import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python

from .models import Contact, OtherContact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class OtherContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherContact
        fields = '__all__'
