from django.contrib import admin
from .models import User,Report,Post, Ban

# Register your models here.
admin.site.register(Post)
admin.site.register(Report)
admin.site.register(User)
admin.site.register(Ban)