from django.contrib import admin
from .models import Estate

class EstateAdmin(admin.ModelAdmin):
    list_filter = ['source']
    list_display = ['title', 'owner']
admin.site.register(Estate, EstateAdmin)
