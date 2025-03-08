from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, id_enseignt=None, role='standard'):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, id_enseignt=id_enseignt, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, role='admin')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('standard', 'Standard'),
        ('admin', 'Admin'),
    ]
    email = models.EmailField(unique=True)
    id_enseignt = models.IntegerField(null=True, blank=True)  
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='standard')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email
    

class OTP(models.Model):
    email = models.EmailField() 
    code = models.CharField(max_length=6,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        expiration_time = self.created_at + timedelta(minutes=5)
        return not self.is_used and timezone.now() <= expiration_time

    def __str__(self):
        return f"OTP for {self.email}: {self.code}"
