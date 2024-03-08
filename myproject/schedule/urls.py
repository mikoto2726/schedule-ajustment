from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('index/', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('answer/<int:pk>/', views.answer, name='answer'),  
    path('success/', views.success, name='success'), 
    path('create/', views.create, name='create'),
    path('results/<int:event_id>/',views.results, name='results'),
    path('delete_date/<str:date_str>/', views.delete_date, name='delete_date'),
    path('delete_all_dates/', views.delete_all_dates, name='delete_all_dates'),
    path('delete_all_event/', views.delete_all_event, name='delete_all_event'),
]