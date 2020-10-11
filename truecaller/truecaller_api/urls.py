from django.urls import path
from truecaller_api import views


urlpatterns = [
    path('contact/', views.ContactList.as_view()),
    path('add_new_contact/', views.OtherContactList.as_view()),
]
