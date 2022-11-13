"""Defines URL patterns for cal app. (calendar)"""

from django.urls import path

from . import views

app_name = 'cal'
urlpatterns = [
  # Calendar page
  path('cal/', views.cal, name='cal'),
  # Edit cal
  path('edit_cal/<int:calday_id>/', views.edit_cal, name='edit_cal'),
  # New cal
  path('new_cal/<int:cal_year>/<int:cal_month>/<int:cal_day>/', views.new_cal, name='new_cal'),
  # Edit all cal
  path('edit_all_cal/', views.edit_all_cal, name='edit_all_cal'),
]