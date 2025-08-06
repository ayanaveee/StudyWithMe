from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('sessions/', views.sessions, name='sessions'),
    path('goals/', views.goals_view, name='goals'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('materials/', views.study_materials, name='study_materials'),
    path('materials/<int:material_id>/', views.study_material_detail_view, name='study_material_detail'),
    path('materials/<int:material_id>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorite_materials_view, name='favorite_materials'),
]



