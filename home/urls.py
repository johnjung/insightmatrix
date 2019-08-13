from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('project/list/', views.ProjectList.as_view(), name='project_list'),
    path('project/create', views.ProjectCreate.as_view(), name='project_create'),
    path('project/<int:pk>/', views.ProjectDetail.as_view(), name='project_detail')
]
