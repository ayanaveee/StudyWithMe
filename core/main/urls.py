from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about, name='about'),
    path('achievements/', views.achievements_view, name='achievements'),

    path('materials/', views.study_materials_view, name='study_materials'),
    path('materials/<int:material_id>/', views.study_material_detail_view, name='study_material_detail'),

    path('goals/', views.goals_list, name='goals'),
    path('goals/<int:pk>/edit/', views.edit_goal, name='edit_goal'),
    path('goals/<int:pk>/complete/', views.mark_goal_completed, name='mark_goal_completed'),
    path('goals/<int:pk>/delete/', views.delete_goal, name='delete_goal'),

    path('materials/<int:material_id>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorite_materials_view, name='favorite_materials'),
    path('favorites/remove/<int:material_id>/', views.remove_favorite, name='remove_favorite'),
    path('favorites/<int:material_id>/', views.favorite_material_detail_view, name='favorite_material_detail'),

]
