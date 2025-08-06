from django.contrib import admin
from .models import (
    StudySession,
    Goal,
    Note,
    Achievement,
    Category,
    StudyMaterial,
    StudyMaterialCategory,
    TopicProgress,
    FavoriteMaterial,
)

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'start_time', 'end_time', 'duration', 'note')
    search_fields = ('user__username', 'goal__title', 'note')
    list_filter = ('start_time', 'end_time', 'goal__category')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category', 'created_at', 'deadline')
    search_fields = ('user__username', 'title')
    list_filter = ('category', 'deadline')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at', 'updated_at')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'code', 'date_earned')
    search_fields = ('user__username', 'title', 'code')
    list_filter = ('date_earned',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'category', 'created_at')
    search_fields = ('title', 'created_by__username')
    list_filter = ('category', 'created_at')

@admin.register(StudyMaterialCategory)
class StudyMaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'material', 'completed', 'completed_at')
    search_fields = ('user__username', 'material__title')
    list_filter = ('completed', 'completed_at')

@admin.register(FavoriteMaterial)
class FavoriteMaterialAdmin(admin.ModelAdmin):
    list_display = ('user', 'material', 'added_at')
    search_fields = ('user__username', 'material__title')
    list_filter = ('added_at',)
