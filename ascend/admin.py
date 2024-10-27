from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(YoutubeContent)
admin.site.register(Resources)
admin.site.register(Courses)