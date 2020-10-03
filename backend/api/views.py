import json

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import status, viewsets, permissions, mixins
from rest_framework.views import exception_handler
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from rest_framework_simplejwt.views import TokenObtainPairView

import pypco

from . import serializers, models
from .permissions import IsAuthenticatedOrWriteOnly


class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegistrationSerializer
    queryset = models.Registration.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class EventLocationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventLocationSerializer
    queryset = models.EventLocation.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class HostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    permission_classes = [
        IsAuthenticatedOrWriteOnly
    ]

    def create(self, request, *args, **kwargs):
        try:
            existing_host = self.queryset.get(email=request.data['email'], first_name=request.data['firstName'], last_name=request.data['lastName'])
        except Exception as e:
            existing_host = None
        if (existing_host):
            serializer = self.get_serializer(existing_host)
            return Response(serializer.data, status=status.HTTP_208_ALREADY_REPORTED)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostRSVPViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HostRSVPSerializer
    queryset = models.HostRSVP.objects.all()
    permission_classes = [
        IsAuthenticatedOrWriteOnly
    ]


class GuestViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.GuestSerializer
    queryset = models.Guest.objects.all()
    permission_classes = [
        IsAuthenticatedOrWriteOnly
    ]

    def create(self, request, *args, **kwargs):
        """
        checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super().create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GuestGradeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GuestGradeSerializer
    queryset = models.GuestGrade.objects.all().order_by('order')
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class GuestRSVPViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.GuestRSVPSerializer
    queryset = models.GuestRSVP.objects.all()
    permission_classes = [
        IsAuthenticatedOrWriteOnly
    ]

    def create(self, request, *args, **kwargs):
        """
        checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        guest_rsvps_raw = request.data
        event = models.Event.objects.get(pk=guest_rsvps_raw[0]['event'])
        existing_rsvps = []

        for i, rsvp in enumerate(guest_rsvps_raw):
            newly_created_guest = models.Guest.objects.get(pk=rsvp['guest'])

            possible_duplicate_guests = models.Guest.objects.filter(
                first_name=newly_created_guest.first_name,
                last_name=newly_created_guest.last_name,
                host=newly_created_guest.host,
                grade=newly_created_guest.grade,
                variant=newly_created_guest.variant
            )

            for duplicate in possible_duplicate_guests:
                rsvps = list(self.queryset.filter(guest=duplicate, event=event))
                existing_rsvps += rsvps
                if len(rsvps) > 0:
                    # Remove any Guests that may exist by the same host to the same event
                    # to prevent duplicate guest registering.
                    # This has the consequence of not being able to reconcile a person re-registering
                    # someone they forgot.
                    # They should contact IT/us instead if this is the case.
                    guest_rsvps_raw.pop(i)
                    if newly_created_guest:
                        newly_created_guest.delete()

        if len(guest_rsvps_raw) > 0:
            serializer = self.get_serializer(data=guest_rsvps_raw, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            serializer = self.get_serializer(existing_rsvps, many=True)
            return Response(serializer.data, status=status.HTTP_208_ALREADY_REPORTED)


# TODO: Have email be customizable via a settings table.
from rest_framework.decorators import api_view, permission_classes

@permission_classes((IsAuthenticatedOrWriteOnly,))
@api_view(['POST',])
def send_confirmation_email(request, *args, **kwargs):
    data = json.loads(request.body.decode('utf-8'))
    host_id = data['host']
    event_id = data['event']

    try:
        event = models.Event.objects.get(pk=event_id)
    except:
        return Response({ 'message': 'Event does not exist, cannot send confirmation.' }, status=status.HTTP_400_BAD_REQUEST)

    try:
        host = models.Host.objects.get(pk=host_id)
    except:
        return Response({ 'message': 'Host does not exist, cannot send confirmation.' }, status=status.HTTP_400_BAD_REQUEST)

    guest_rsvps = models.GuestRSVP.objects.filter(guest__host=host, event=event)
    guest_count = guest_rsvps.count()

    try:
        date_str = event.start.strftime('%A, %B %-d, %Y')
        guest_rsvp_str = ''
        for rsvp in guest_rsvps:
            guest_rsvp_str += f'\tChild ({rsvp.guest.grade}) on {rsvp.event}\n'

        to = [host.email]
        if event.use_custom_email_subject and event.custom_email_subject:
            subject = event.custom_email_subject
        else:
            subject = f"Your { event.start.strftime('%A') } RSVP Confirmation"
        message = f'Hey {host.first_name}!\n\nWe got your RSVP for your children on {date_str}.\n\nIn total you registered {guest_count} kids. Here is a summary:\n\n{guest_rsvp_str}\nWe look forward to seeing you! Please leave enough time to check your children in at the right locations!\nPlease know that while preregistration tells our kids team to expect your child, capacity is limited due to Covid restrictions and final check-in at arrival will confirm availability.'

        send_mail(
            subject,
            message,
            f'Member Support <{settings.EMAIL_HOST_USER}>',
            to,
            fail_silently=False
        )
    except Exception as e:
        print(e)
        return Response({ 'message': 'Cannot send confirmation.' }, status=status.HTTP_400_BAD_REQUEST)

    return Response({ 'message': 'Successfully sent e-mail.' }, status=status.HTTP_200_OK)
