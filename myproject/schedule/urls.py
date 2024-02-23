from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('schedule/', views.schedule, name='schedule'),  # スケジュールフォームへのパス
    path('success/', views.success, name='success'),  # 成功ページへのパス
    path('create_date/', views.create_date, name='create_date'),
    path('view_results/',views.view_results, name='view_results'),

]
