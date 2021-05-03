from django.contrib import admin

from .models import News, Person, Person_with_sites

admin.site.register(News)
admin.site.register(Person)
admin.site.register(Person_with_sites)
