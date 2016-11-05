from django.contrib import admin
from .models import ZipCode


class ZipCodeAdmin(admin.ModelAdmin):
    model = ZipCode
    search_fields = ('zip_code',)
    
admin.site.register(ZipCode, ZipCodeAdmin)
