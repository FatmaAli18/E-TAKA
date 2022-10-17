from email.policy import default
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
CATEGORY = (
    ('Mobile Phones', 'Mobile Phones'),
    ('Laptops', 'Laptops'),
    ('Televisions', 'Televisions'),
)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='images/profile', null=True)
    
    def __str__(self):
        return f'{self.staff}-Profile'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/products', null=True)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    def __str__(self):
        return self.name
        
    

class Meta:
        verbose_name_plural = 'Product'

            
        


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return self.name.name
    
  
class  Meta:
    verbose_name_plural = 'Order'
    
   
        

