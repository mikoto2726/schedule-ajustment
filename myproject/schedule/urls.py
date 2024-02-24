from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('schedule/', views.schedule, name='schedule'),  # スケジュールフォームへのパス
    path('success/', views.success, name='success'),  # 成功ページへのパス
    path('create_date/', views.create_date, name='create_date'),
    path('view_results/',views.view_results, name='view_results'),
    path('delete_date/<str:date_str>/', views.delete_date, name='delete_date'),
    path('delete_all_dates/', views.delete_all_dates, name='delete_all_dates'),
]
