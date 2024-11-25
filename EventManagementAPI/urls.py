"""
URL configuration for EventManagementAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import path
from Event.views import (
    EventListCreateView,
    EventDetailView,
    RegisterAttendeeView,
    CheckInAttendeeView,
    ListAttendeesView,
    BulkCheckInView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('attendees/register/', RegisterAttendeeView.as_view(), name='register-attendee'),
    path('attendees/<int:attendee_id>/check-in/', CheckInAttendeeView.as_view(), name='check-in-attendee'),
    path('events/<int:event_id>/attendees/', ListAttendeesView.as_view(), name='list-attendees'),
    path('attendees/bulk-check-in/', BulkCheckInView.as_view(), name='bulk-check-in'),
]

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

