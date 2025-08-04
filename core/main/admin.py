from django.contrib import admin
from .models import StudySession, Goal, Note, Achievement

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'created_at')
    search_fields = ('user__username', 'note')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'start_date', 'end_date', 'created_at')
    search_fields = ('user__username', 'target')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'content')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date_earned')
    search_fields = ('user__username', 'title')
