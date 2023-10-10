from django.contrib import admin
from main_app.models import Mailing, Message, Client
# Register your models here.

admin.site.register([Mailing,Message,Client])

