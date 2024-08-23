from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxLengthValidator
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email kiritishingiz shart')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **kwargs)
        
        
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    
    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['email']
        

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_time']
        

class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='shop_category')
    description = models.TextField(
        validators=[
            MaxLengthValidator(
                limit_value=2000,
                message='You can\'t input longer text than 2000 characters'
            )
        ]
    )
    price = models.DecimalField(max_digits=15, decimal_places=3)
    image = models.ImageField(upload_to='shop/image/')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_time']


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cancel = models.BooleanField(default=False)
    
    def get_total(self):
        return self.quantity* int(self.product.price)
    
    def __str__(self):
        return self.product.title
    
    class Meta:
        ordering = ['-created_time']


class Commet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='commet_shop')
    body = models.TextField(
        validators=[
            MaxLengthValidator(
                limit_value=2000,
                message='You can\'t input longer text than 2000 characters'
            )
        ]
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='child'
    )