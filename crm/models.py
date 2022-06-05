from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    phone = models.IntegerField(default=0, null=True)
    profile_image = models.ImageField(default='default.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Fashion','Fashion'),
        ('Mobiles and Tablets','Mobiles and Tablets'),
        ('Electronics','Electronics'),
        ('Books','Books'),
        ('Movie Tickets','Movie Tickets'),
        ('Baby Products','Books'),
        ('Books','Baby Products'),
        ('Groceries','Groceries'),
        ('Home Furnishings','Home Furnishings'),
        ('Jewellery','Jewellery'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField(default=0, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    tags = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.product)