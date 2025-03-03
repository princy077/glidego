from django.contrib import admin
from .models import Destination, Activity, UserPreference, Review

admin.site.register(Destination)
admin.site.register(Activity)
admin.site.register(UserPreference)
admin.site.register(Review)
