from django.db.models import TextChoices

class UserRoleEnum(TextChoices):
    STUDENT = 'student', 'Студент'
    ADMIN = 'admin', 'Администратор'
