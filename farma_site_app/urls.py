"""Defines URL patterns for farma_site_app."""

from django.urls import path

from . import views

app_name = 'farma_site_app'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all blog entries.
    path('blog/', views.blog, name='blog'),
    # Detail page for a single entry.
    path('blog/<int:entry_id>/', views.entry, name='entry'),
    # Page for adding a new blog entry.
    path('new_entry/', views.new_entry, name='new_entry'),
    # Page for editing an entry.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # Page for contacts.
    path('contacto/', views.contacto, name='contacto'),
    # Page for success of having sent email.
    path('sucesso/', views.sucesso, name='sucesso'),
]
