from django.urls import path
from . import views

app_name = "cards_app"

urlpatterns = [
    path('', views.main_manage_page, name='main')
]
