from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Seen(models.Model):
    user = models.OneToOneField(User)
    seen = models.DateTimeField(auto_now=True)


admin.site.register(Seen, list_display=('user', 'seen'))
