from django.db import models
from django.contrib.auth import get_user_model

MyUser = get_user_model()

class StudySession(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    date = models.DateField(verbose_name='Дата сессии')
    note = models.TextField(blank=True, null=True, verbose_name='Заметка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Session of {self.user.username} on {self.date}"

    class Meta:
        verbose_name = 'Учебная сессия'
        verbose_name_plural = 'Учебные сессии'


class Achievement(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    title = models.CharField(max_length=100, verbose_name='Название достижения')
    description = models.TextField(blank=True, verbose_name='Описание достижения')
    date_earned = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')

    def __str__(self):
        return f"{self.title} — {self.user.username}"

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'


class Goal(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    target = models.CharField(max_length=255, verbose_name='Цель')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.user.username}'s Goal – {self.target}"

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'


class Note(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"Note by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
