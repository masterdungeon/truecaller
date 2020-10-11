from django.contrib import admin

from .models import Contact
from .models import OtherContact

admin.site.register(Contact)
admin.site.register(OtherContact)
