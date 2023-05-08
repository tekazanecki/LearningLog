"""Definiuje wzorce adresów URL dla learning_logs."""

from django.urls import path
from . import views

app_name = 'learning_logs'

urlpatterns = [
    # strona główna
    path('', views.index, name='index'),
    #wyświetlanie tematów
    path('topics', views.topics, name='topics'),
    path('topics/<topic_id>', views.topic, name='topic'),
    path('new_topic', views.new_topic, name='new_topic'),
    path('new_entry/<topic_id>', views.new_entry, name='new_entry'),
    path('edit_entry/<entry_id>', views.edit_entry, name='edit_entry'),
]