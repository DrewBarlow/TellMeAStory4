from django.contrib import admin
from .models import Post,Report,UserTable

#Register each table into the admin site
admin.site.register(Post)
admin.site.register(Report)
admin.site.register(UserTable)