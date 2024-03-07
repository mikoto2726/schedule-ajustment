from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('create/', views.your_view, name='your_view'),
    path('success/', views.success, name='success'),
    path('delete_all_dates/', views.delete_all_dates, name='delete_all_dates'),
]
