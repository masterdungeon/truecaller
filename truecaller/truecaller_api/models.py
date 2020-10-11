from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    name = models.CharField(max_length=256, blank=False)
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    phone = PhoneNumberField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + str(self.phone)

class OtherContact(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    phone = PhoneNumberField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.name + " - " + str(self.phone)
