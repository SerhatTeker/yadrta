from django.contrib import admin

from .models import Category, Tag, Task

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Task)
