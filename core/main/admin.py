from django.contrib import admin
from .models import (
    StudySession,
    Goal,
    Note,
    Achievement,
    Category,
    StudyMaterial,
    StudyMaterialCategory,
)

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'start_time', 'end_date', 'note')
    search_fields = ('user__username', 'note', 'goal__title')
    list_filter = ('start_time', 'end_date')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'deadline', 'category')
    search_fields = ('user__username', 'title')
    list_filter = ('category', 'deadline')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    search_fields = ('user__username', 'content')
    list_filter = ('updated_at', 'created_at')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date_earned')
    search_fields = ('user__username', 'title')
    list_filter = ('date_earned',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'category', 'created_at')
    search_fields = ('title',  'created_by__username')
    list_filter = ('category', 'created_at')

@admin.register(StudyMaterialCategory)
class StudyMaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
