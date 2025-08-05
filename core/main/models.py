from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import CharField

MyUser = get_user_model()

class StudySession(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    goal = models.ForeignKey('Goal', on_delete=models.CASCADE, verbose_name='Цель')
    note = models.TextField(blank=True, null=True, verbose_name='Заметка')
    start_time = models.DateTimeField(verbose_name='Дата создания')
    end_date = models.DateTimeField(verbose_name='Дата сессии')

    def __str__(self):
        return f"Session of {self.user.username} on {self.end_date}"

    class Meta:
        verbose_name = 'Учебная сессия'
        verbose_name_plural = 'Учебные сессии'

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Achievement(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Пользователь')
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
    title = models.CharField(max_length=255, verbose_name='Цель')
    related_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Подцель')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала')
    deadline = models.DateTimeField(verbose_name='Дата окончания')

    def __str__(self):
        return f"{self.user.username}'s Goal – {self.target}"

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

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
    video = models.FileField(upload_to='videos/', verbose_name='Видео')
    topic = models.CharField(max_length=100, verbose_name="Тема")
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Учебный материал"
        verbose_name_plural = "Учебные материалы"

class StudyMaterialCategory(models.Model):
    title = CharField(max_length=20)

    class Meta:
        verbose_name = "Категория материала"
        verbose_name_plural = "Категории материалов"
