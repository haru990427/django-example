from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError("이메일은 필수로 입력해야 합니다.")

        if not nickname:
            raise ValueError("닉네임은 필수로 입력해야 합니다.")

        if not password:
            raise ValueError("비밀번호는 필수로 입력해야 합니다.")

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None):
        if not email:
            raise ValueError("이메일은 필수로 입력해야 합니다.")

        if not nickname:
            raise ValueError("닉네임은 필수로 입력해야 합니다.")

        if not password:
            raise ValueError("비밀번호는 필수로 입력해야 합니다.")

        user = self.create_user(
            email=email,
            password=password,
            nickname=nickname
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    coin = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' # User Model에서 사용할 고유 식별자
    REQUIRED_FIELDS = ['nickname'] # createsuperuser로 관리자를 생성할 때 입력받을 필드
