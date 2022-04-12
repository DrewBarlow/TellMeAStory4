from django.contrib import admin
from .models import User,Report,Post

# Register your models here.
admin.site.register(Post)
admin.site.register(Report)
admin.site.register(User)