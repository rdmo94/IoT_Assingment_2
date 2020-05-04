from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password, meterID):
        if not email:
            raise ValueError("User must have a valid email address")
        if not username:
            raise ValueError("User must have a valid username")
        if not meterID:
            raise ValueError("user must have a valid meterID")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            meterID=meterID,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, meterID):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            meterID=meterID,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    meterID = models.CharField(unique=True, max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'meterID']

    objects = MyAccountManager()

    def __str__(self):
        return self.email + ', ' + self.meterID

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.username

    def meterIdsAsList(self):
        return [i for i in [int(n) for n in self.meterID.split()] if i > -1]

    def containsId(self, id):
        return id in self.meterIdsAsList()


