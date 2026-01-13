from django.contrib import admin
from .models import Event, Location
from news_app.models import News
from users_app.models import UserProfile, Job
from role_app.models import Role, RoleInEvent

admin.site.register(Event)
admin.site.register(Location)
admin.site.register(News)
admin.site.register(Job)
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(RoleInEvent)
