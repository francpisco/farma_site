from django.contrib import admin

from .models import CalDia

# admin.site.register(CalDia)

@admin.register(CalDia)
class CalDiaAdmin(admin.ModelAdmin):
  ordering = ['day']