"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


router = DefaultRouter()
router.register('registrations', views.RegistrationViewSet)
router.register('event-locations', views.EventLocationViewSet)
router.register('events', views.EventViewSet)
router.register('hosts', views.HostViewSet)
router.register('guests', views.GuestViewSet)
router.register('guest-grades', views.GuestGradeViewSet)
router.register('host-rsvp', views.HostRSVPViewSet)
router.register('guest-rsvp', views.GuestRSVPViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('mail-confirmation/', views.send_confirmation_email)
]
