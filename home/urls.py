from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/create', views.project_create, name='project_create'),
    path('project/list/', views.ProjectList.as_view(), name='project_list'),
    path('project/update/<int:pk>/', views.project_update, name='project_update'),
]
