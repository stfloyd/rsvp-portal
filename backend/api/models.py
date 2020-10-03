from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name, last_name=last_name,
            is_staff=is_staff, is_active=True,
            is_superuser=is_superuser, last_login=now,
            date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name):
        return self._create_user(email, password, first_name, last_name, False, False)

    def create_superuser(self, email, password, first_name, last_name):
        return self._create_user(email, password, first_name, last_name, True, True)


class User(AbstractUser):
    objects = UserManager()

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Registration(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    #image_url = models.CharField(max_lengt=255)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'registration'
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
        ordering = ['pk']


class EventLocation(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='event_locations')

    name = models.CharField(max_length=255)
    max_occupancy = models.IntegerField()#null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'event_location'
        verbose_name = 'Event Location'
        verbose_name_plural = 'Event Locations'


class Event(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='events')

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    slug = models.CharField(max_length=32)

    location = models.ForeignKey('EventLocation', on_delete=models.CASCADE)

    # Override default max_occupancy
    max_occupancy = models.IntegerField(null=True, blank=True)

    collect_guest_names = models.BooleanField(default=False)

    children_only = models.BooleanField(default=True)

    use_custom_email_subject = models.BooleanField(default=False)
    custom_email_subject = models.CharField(max_length=255, null=True, blank=True)

    excerpt = models.CharField(max_length=255, null=True, blank=True)

    start = models.DateTimeField()
    end = models.DateTimeField()

    open = models.DateTimeField()
    close = models.DateTimeField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration} - {self.title} @ {self.start.strftime('%Y-%m-%d')}"

    @property
    def current_occupancy(self):
        return self.guest_attendances.count() #+ self.host_attendances.count()

    @property
    def grade_occupancies(self):
        occupancies = []
        grade_levels = GuestGrade.objects.filter(registration=self.registration)

        for gl in grade_levels:
            rsvps = len(list(GuestRSVP.objects.filter(guest__grade=gl, event=self)))
            occupancies.append((gl, rsvps))

        return occupancies

    @property
    def max_capacity(self):
        capacity = 0
        for g in self.grade_occupancies:
            capacity += g[0].max_occupancy
        return capacity

    class Meta:
        db_table = 'event'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class Host(models.Model):
    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    email = models.EmailField(_('email address'))
    phone_number = models.CharField(_('phone number'), max_length=20, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def number_of_guests(self):
        return self.guests.count()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'host'
        verbose_name = 'Host'
        verbose_name_plural = 'Hosts'
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name', 'email'], name='unique_host')
        ]


class GuestType(models.IntegerChoices):
    TYPE_CHILD = 0, _('Child')
    TYPE_ADULT = 1, _('Adult')

    __empty__ = _('(Unknown)')


class GuestGrade(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='guest_grades')

    name = models.CharField(_('name'), max_length=48)
    max_occupancy = models.IntegerField()

    order = models.IntegerField(default=-1)

    @property
    def current_occupancy(self):
        return GuestRSVP.objects.filter(guest__grade=self).count()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'guest_grade'
        verbose_name = 'Guest Grade'
        verbose_name_plural = 'Guest Grades'
        constraints = [
            models.UniqueConstraint(fields=['registration', 'name'], name='unique_grades')
        ]


class Guest(models.Model):
    host = models.ForeignKey(Host, related_name='guests', on_delete=models.CASCADE)

    first_name = models.CharField(_('first name'), max_length=255, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, null=True, blank=True)

    grade = models.ForeignKey(GuestGrade, null=True, on_delete=models.CASCADE)

    variant = models.IntegerField(choices=GuestType.choices)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'guest'
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name', 'host'], name='unique_guest')
        ]


class HostRSVP(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='host_attendances')
    host = models.ForeignKey('Host', null=True, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'host_rsvp'
        verbose_name = 'Host RSVP'
        verbose_name_plural = 'Host RSVP\'s'
        constraints = [
            models.UniqueConstraint(fields=['event', 'host'], name='unique_host_attendance')
        ]


class GuestRSVP(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='guest_attendances')
    guest = models.ForeignKey('Guest', null=True, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'guest_rsvp'
        verbose_name = 'Guest RSVP'
        verbose_name_plural = 'Guest RSVP\'s'
        constraints = [
            models.UniqueConstraint(fields=['event', 'guest'], name='unique_guest_attendance')
        ]


class Settings(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)

    class Meta:
        db_table = 'settings'
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'
