from rest_framework import serializers

from . import models


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Registration
        fields = ('id', 'title', 'subtitle', 'slug', 'hide')


class HostSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    phoneNumber = serializers.CharField(source='phone_number', allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = models.Host
        fields = ('id', 'firstName', 'lastName', 'email', 'phoneNumber')


class GuestSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name', allow_null=True, allow_blank=True, required=False)
    lastName = serializers.CharField(source='last_name', allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = models.Guest
        fields = ('id', 'host', 'firstName', 'lastName', 'variant', 'grade')


class GuestGradeSerializer(serializers.ModelSerializer):
    maxOccupancy = serializers.IntegerField(source='max_occupancy')

    class Meta:
        model = models.GuestGrade
        fields = ('id', 'name', 'registration', 'maxOccupancy', 'order')


class EventLocationSerializer(serializers.ModelSerializer):
    maxOccupancy = serializers.IntegerField(source='max_occupancy')

    class Meta:
        model = models.EventLocation
        fields = ('id', 'name', 'maxOccupancy')


class EventSerializer(serializers.ModelSerializer):
    maxOccupancy = serializers.IntegerField(source='max_occupancy')
    gradeOccupancies = serializers.SerializerMethodField()
    collectGuestNames = serializers.BooleanField(source='collect_guest_names')
    childrenOnly = serializers.BooleanField(source='children_only')
    useCustomEmailSubject = serializers.BooleanField(source='use_custom_email_subject')
    customEmailSubject = serializers.CharField(source='custom_email_subject')

    def get_gradeOccupancies(self, obj):
        serialized = []

        for g in obj.grade_occupancies:
            g_s = GuestGradeSerializer(g[0])
            data = g_s.data
            data['currentOccupancy'] = g[1]
            serialized.append(data)

        return sorted(serialized, key=lambda obj: obj['order'])

    class Meta:
        model = models.Event
        fields = ('id', 'registration', 'slug', 'title', 'subtitle', 'excerpt', 'location', 'maxOccupancy', 'start', 'end', 'open', 'close', 'gradeOccupancies', 'collectGuestNames', 'childrenOnly', 'useCustomEmailSubject', 'customEmailSubject')


class HostRSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HostRSVP
        fields = ('id', 'host', 'event')


class GuestRSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GuestRSVP
        fields = ('id', 'guest', 'event')
