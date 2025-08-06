from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import CharField

MyUser = get_user_model()

class StudySession(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    goal = models.ForeignKey('Goal', on_delete=models.CASCADE, verbose_name='Цель')
    note = models.TextField(blank=True, null=True, verbose_name='Заметка')
    start_time = models.DateTimeField(verbose_name='Дата создания')
    end_time = models.DateTimeField(verbose_name='Дата сессии')
    duration = models.DurationField(blank=True, null=True, verbose_name='Длительность')

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Session of {self.user.username} on {self.end_time}"

    class Meta:
        verbose_name = 'Учебная сессия'
        verbose_name_plural = 'Учебные сессии'


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория цели'
        verbose_name_plural = 'Категории целей'


class Achievement(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    code = models.CharField(max_length=50, unique=True, verbose_name="Код условия", default='default_code')
    title = models.CharField(max_length=100, verbose_name='Название достижения')
    description = models.TextField(blank=True, verbose_name='Описание достижения')
    date_earned = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')

    def __str__(self):
        return f"{self.title} — {self.user.username}"

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'


class Goal(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    title = models.CharField(max_length=255, verbose_name='Цель')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала')
    deadline = models.DateTimeField(verbose_name='Дата окончания')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено')

    def __str__(self):
        return f"{self.user.username}'s Goal – {self.title}"

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'


class TopicProgress(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    material = models.ForeignKey('StudyMaterial', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        status = "Изучено" if self.completed else "В процессе"
        return f"{self.user.username} — {self.material.title} ({status})"

    class Meta:
        verbose_name = "Прогресс по теме"
        verbose_name_plural = "Прогресс по темам"


class FavoriteMaterial(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    material = models.ForeignKey('StudyMaterial', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — избранное: {self.material.title}"

    class Meta:
        verbose_name = "Избранный материал"
        verbose_name_plural = "Избранные материалы"


class Note(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"Note by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'


class StudyMaterial(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    video = models.TextField(blank=True, null=True, verbose_name='Видео')
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    category = models.ForeignKey('StudyMaterialCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='materials', verbose_name="Категория")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Учебный материал"
        verbose_name_plural = "Учебные материалы"


class StudyMaterialCategory(models.Model):
    title = CharField(max_length=100)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
