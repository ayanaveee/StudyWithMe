from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .choices import UserRoleEnum

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("У пользователя должна быть почта")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username, email=email, password=password)
        user.role = UserRoleEnum.ADMIN
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, verbose_name='Имя пользователя')
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='user_avatar/', null=True, blank=True, verbose_name='Аватарка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_2fa_enabled = models.BooleanField(default=False, verbose_name='Двухфакторная аутентификация')

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    role = models.CharField(
        max_length=20,
        choices=UserRoleEnum.choices,
        default=UserRoleEnum.STUDENT,
        verbose_name='Роль'
    )
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.role == UserRoleEnum.ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class OTP(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    code = models.CharField(max_length=6, verbose_name='Код подтверждения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"OTP for {self.user.email} - {self.code}"

    class Meta:
        verbose_name = 'Одноразовый код'
        verbose_name_plural = 'Одноразовые коды'
