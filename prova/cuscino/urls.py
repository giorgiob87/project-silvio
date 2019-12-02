
from django.urls import path

from . import views

app_name = 'cuscino'
urlpatterns = [
    path('', views.index, name='index'),
]
