from django.contrib import admin
from .models import User, POST, USERPROFILE

# Register your models here.
admin.site.register(User)
admin.site.register(POST)
admin.site.register(USERPROFILE)


