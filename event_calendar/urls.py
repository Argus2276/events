"""
URL configuration for event_calendar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include

from calendar_app.V1.views import EventView, NewsCreateListView, EventListCreateView
from mailings_app.views import RequestsListView, RequestsRetrieveUpdateDestroyView
from role_app.views import RoleInEventView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/events/", EventListCreateView.as_view(), name="event-list"),
    path("api/v1/events/<int:pk>/", EventView.as_view(), name="event-change"),
    path("roles/", RoleInEventView.as_view(), name="role-list"),
    path("api/v1/news/", NewsCreateListView.as_view(), name="news-list"),
    path("api/mailings/", RequestsListView.as_view(), name="request-list"),
    path(
        "api/mailings/<int:pk>/",
        RequestsRetrieveUpdateDestroyView.as_view(),
        name="request-interact",
    ),
]
