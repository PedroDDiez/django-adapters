from django.urls import path

from . import views

urlpatterns = [
    path('<str:base_currency>/', views.dashboard, name='index'),
]
