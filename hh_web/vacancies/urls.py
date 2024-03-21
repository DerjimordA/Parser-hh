from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('database/', views.database_view, name='database'),
    path('collect_vacancies/', views.collect_vacancies, name='collect_vacancies'),
    path('filter_vacancies/', views.filter_vacancies, name='filter_vacancies'),
]
