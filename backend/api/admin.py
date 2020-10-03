from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html

from . import models, forms


class UserInline(admin.TabularInline):
    model = models.User.groups.through
    #raw_id_fields = ('user',)  # optional, if you have too many users


class GroupInline(admin.TabularInline):
    model = DjangoGroup


class GroupAdmin(DjangoGroupAdmin):
    inlines = [UserInline]


class GuestInline(admin.TabularInline):
    model = models.Guest


class GuestRSVPInline(admin.StackedInline):
    model = models.GuestRSVP
    extra = 1
    max_num = 1


class GuestGradeInline(admin.TabularInline):
    model = models.GuestGrade
    fields = ['name', 'current_occupancy', 'max_occupancy']
    readonly_fields = ['current_occupancy']


class HostInline(admin.TabularInline):
    model = models.Host


class HostRSVPInline(admin.TabularInline):
    model = models.HostRSVP


class UserAdmin(admin.ModelAdmin):
    change_form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form = self.change_form
        else:
            self.form = self.add_form
        return super().get_form(request, obj, **kwargs)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_display_links = ('title',)
    inlines = [
        GuestGradeInline
    ]


class EventLocationAdmin(admin.ModelAdmin):
    list_display = ('registration', 'name', 'max_occupancy')
    search_fields = ('name',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_to_registration', 'start', 'end', 'current_occupancy', 'occupancy_limit')
    search_fields = ('title',)

    def link_to_registration(self, obj):
        link = reverse("admin:api_registration_change", args=[obj.registration.id])
        return format_html('<a href="{}">{}</a>', link, obj.registration)
    link_to_registration.short_description = 'Registration'

    def link_to_location(self, obj):
        link = reverse("admin:api_eventlocation_change", args=[obj.location.id])
        return format_html('<a href="{}">{}</a>', link, obj.location)
    link_to_location.short_description = 'Location'

    def occupancy_limit(self, obj):
        return obj.max_capacity

    def current_occupancy(self, obj):
        return obj.current_occupancy


class HostAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'link_to_email', 'number_of_guests')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'email')

    inlines = [
        GuestInline,
        HostRSVPInline
    ]

    def link_to_email(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
    link_to_email.short_description = 'E-mail Address'


class HostRSVPAdmin(admin.ModelAdmin):
    list_display = ('id', 'link_to_event', 'link_to_host')

    def link_to_event(self, obj):
        link = reverse("admin:api_event_change", args=[obj.event.id])
        return format_html('<a href="{}">{}</a>', link, obj.event)
    link_to_event.short_description = 'Event'

    def link_to_host(self, obj):
        link = reverse("admin:api_host_change", args=[obj.host.id])
        return format_html('<a href="{}">{}</a>', link, obj.host)
    link_to_host.short_description = 'Host'


class GuestAttendanceFilter(admin.SimpleListFilter):
    title = 'events'
    parameter_name = 'event'

    def lookups(self, request, model_admin):
        list_tuple = []
        for event in models.Event.objects.all():
            list_tuple.append((event.id, event.title))
        return list_tuple

    def queryset(self, request, queryset):
        if self.value():
            event = models.Event.objects.get(pk=self.value())
            guest_ids = event.guest_attendances.values_list('guest_id', flat=True)
            guests = models.Guest.objects.filter(pk__in=guest_ids)
            return guests
        else:
            return queryset


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'link_to_host', 'grade', 'variant')
    list_display_links = ('first_name', 'last_name')
    list_filter = (GuestAttendanceFilter, 'grade__name', 'variant',)
    search_fields = ('first_name', 'last_name', 'host__first_name', 'host__last_name')
    inlines = [
        GuestRSVPInline
    ]

    def link_to_host(self, obj):
        link = reverse("admin:api_host_change", args=[obj.host.id])
        return format_html('<a href="{}">{}</a>', link, obj.host)
    link_to_host.short_description = 'Host'


class GuestGradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_to_registration', 'current_occupancy', 'max_occupancy')
    list_filter = ('registration',)
    search_fields = ('name',)

    def link_to_registration(self, obj):
        link = reverse("admin:api_registration_change", args=[obj.registration.id])
        return format_html('<a href="{}">{}</a>', link, obj.registration)
    link_to_registration.short_description = 'Registration'


class GuestRSVPAdmin(admin.ModelAdmin):
    list_display = ('id', 'link_to_event', 'link_to_host', 'link_to_guest', 'guest_grade')
    list_filter = ('event__registration', 'event', 'guest__grade__name')

    def guest_grade(self, obj):
        return obj.guest.grade
    guest_grade.short_description = 'Guest Grade'

    def link_to_host(self, obj):
        link = reverse('admin:api_host_change', args=[obj.guest.host.id])
        return format_html('<a href="{}">{}</a>', link, obj.guest.host)
    link_to_host.short_description = 'Host'

    def link_to_event(self, obj):
        link = reverse("admin:api_event_change", args=[obj.event.id])
        return format_html('<a href="{}">{}</a>', link, obj.event)
    link_to_event.short_description = 'Event'

    def link_to_guest(self, obj):
        link = reverse("admin:api_guest_change", args=[obj.guest.id])
        return format_html('<a href="{}">{}</a>', link, obj.guest)
    link_to_guest.short_description = 'Guest'


admin.site.unregister(DjangoGroup)
admin.site.register(DjangoGroup, GroupAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Registration, RegistrationAdmin)
admin.site.register(models.EventLocation, EventLocationAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.Guest, GuestAdmin)
admin.site.register(models.GuestGrade, GuestGradeAdmin)
admin.site.register(models.HostRSVP, HostRSVPAdmin)
admin.site.register(models.GuestRSVP, GuestRSVPAdmin)
