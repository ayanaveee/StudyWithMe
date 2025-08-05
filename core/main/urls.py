from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('sessions/', views.sessions, name='sessions'),
    path('goals/', views.goals, name='goals'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('materials/', views.study_materials, name='study_materials'),
    path('materials/<int:pk>/', views.study_material_detail, name='study_material_detail'),
]


