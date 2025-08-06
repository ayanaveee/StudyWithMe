from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about, name='about'),
    path('sessions/', views.sessions_view, name='sessions'),
    #Goals
    path('goals/', views.goals_list, name='goals'),
    path('goals/<int:pk>/edit/', views.edit_goal, name='edit_goal'),

    path('achievements/', views.achievements_view, name='achievements'),
    path('materials/', views.study_materials_view, name='study_materials'),
    path('materials/<int:material_id>/', views.study_material_detail_view, name='study_material_detail'),
    #Favorite
    path('materials/<int:material_id>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorite_materials_view, name='favorite_materials'),
    path('favorites/remove/<int:material_id>/', views.remove_favorite, name='remove_favorite'),
]



