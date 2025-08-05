from .models import Achievement, StudySession
from django.utils import timezone


def check_and_award_achievements(user):
    sessions_count = StudySession.objects.filter(user=user).count()

    achievement_titles = Achievement.objects.filter(user=user).values_list('title', flat=True)

    if sessions_count >= 5 and '5 Study Sessions' not in achievement_titles:
        Achievement.objects.create(
            user=user,
            title='5 Study Sessions',
            description='Вы провели 5 учебных сессий!',
            date_earned=timezone.now()
        )

