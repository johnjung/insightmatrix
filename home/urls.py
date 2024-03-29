from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('label/list/<int:project>/', views.label_list, name='label_list'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/list/', views.ProjectList.as_view(), name='project_list'),
    path('project/update/<int:pk>/', views.project_update, name='project_update'),
    path('similarity/<int:project>/', views.similarity_create, name='similarity_create'),
    path('similarity/list/<int:project>/', views.similarity_list, name='similarity_list')
]
