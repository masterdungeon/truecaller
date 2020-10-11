import jwt, json

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import status, exceptions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Contact, OtherContact
from .serializers import ContactSerializer, OtherContactSerializer


class TokenAuthentication(BaseAuthentication):
    """

    """
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower().decode('UTF-8') != 'bearer':
            return ('', {'Error': "Token is invalid"})

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        try:
            # payload = jwt.decode(token, "SECRET_KEY")
            payload = jwt.decode(token, 'SECRET', algorithms=['HS256'])
            userid = payload['user_id']
            user = User.objects.get(
                id=int(userid),
            )
        except:
            return ('', {'Error': "Token is invalid"})

        return (user, '')

class ContactList(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def get(self, request):
        try:
            auth = TokenAuthentication()
            user, error = auth.authenticate(request)
            if (error):
                return Response(
                    error,
                    status=400,
                    content_type="application/json"
                )
            else:
                contacts = Contact.objects.all()
                response = []
                for contact in contacts:
                    other_contacts = OtherContact.objects.filter(contact=contact.id)
                    response.append({
                        'name': contact.name,
                        'phone': contact.phone.as_e164,
                        'email': contact.email,
                        'linked_contacts': [{'phone':contact.phone.as_e164} for contact in other_contacts]
                    })
                return Response(
                    response,
                    status=200,
                    content_type="application/json"
                )
        except:
            return HttpResponse(
                json.dumps({'Error': "Internal server error"}),
                status=500,
                content_type="application/json"
            )


    def post(self, request):
        auth = TokenAuthentication()
        user, error = auth.authenticate(request)
        if (error):
            return Response(
                error,
                status=400,
                content_type="application/json"
            )
        else:
            try:
                name = request.data.get('name', None)
                email = request.data.get('email', None)
                phone = request.data.get('phone', None)
                contact = Contact(
                    name=name,
                    phone=phone,
                    email=email,
                )
                contact.save()

                response = {
                    'msg': 'Contact saved successfully',
                    'data': request.data
                }
                return Response(
                    response,
                    status=200,
                    content_type="application/json"
                )
            except Exception as e:
                response = {
                    'error': str(e)
                }
                return Response(
                    response,
                    status=400,
                    content_type="application/json"
                )


class OtherContactList(APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    def post(self, request):
        auth = TokenAuthentication()
        user, error = auth.authenticate(request)
        if (error):
            return Response(
                error,
                status=400,
                content_type="application/json"
            )
        else:
            contact_id = request.data.get('contact_id', None)
            phone = request.data.get('phone', None)
            contact = Contact.objects.filter(id=contact_id)
            othercontact = OtherContact(
                contact=contact[0],
                phone=phone,
            )
            othercontact.save()

            response = {
                'msg': 'Contact linked successfully',
                'data': request.data
            }
            return Response(
                response,
                status=200,
                content_type="application/json"
            )
