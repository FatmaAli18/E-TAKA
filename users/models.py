from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY = (
    ('Mobile Phones', 'Mobile Phones'),
    ('Laptops', 'Laptops'),
    ('Televisions', 'Televisions'),
)


class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    image = models.ImageField(default='profile-img2.jpg', upload_to='Profile_Images')

    def __str__(self):
        return f'{self.staff.name}-Profile'


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    image = models.ImageField(default='E-Waste', upload_to='Profile_Images')


class Meta:
    verbose_name_plural = 'Product'

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)


class Meta:
    verbose_name_plural = 'Order'

    def __str__(self):
        return f'{self.staff}-{self.name}'

