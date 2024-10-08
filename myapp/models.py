from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.utils import timezone

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    age = models.IntegerField(default=None, blank=True, null=True, validators=[validators.MinValueValidator(0)])
    phone_number = models.CharField(
        max_length=20,
        default="",
        blank=True,
        null=True,
        validators=[validators.RegexValidator(regex='^[0-9]*$', message='Enter a valid phone number.', code='invalid_number')]
    )  # Only allow numeric values
    address = models.TextField(default="", blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

from django.db import models

class CakeCategory(models.Model):
    category_id = models.AutoField(primary_key=True)  # Auto-incrementing Primary Key
    category_name = models.CharField(max_length=255)  # VARCHAR field for category name

    def __str__(self):
        return self.category_name


class Cake(models.Model):
    CAKE_SIZES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]

    cake_id = models.AutoField(primary_key=True)
    cake_name = models.CharField(max_length=255)
    category = models.ForeignKey(CakeCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=6, choices=CAKE_SIZES)
    description = models.TextField()
    image = models.ImageField(upload_to='cakes/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cake_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s cart"
    
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled')
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Credit Card', 'Credit Card'),
        ('Jazz Cash', 'Jazz Cash'),
        ('Easy Paisa', 'Easy Paisa')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

# OrderItems Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem {self.id} - {self.cake.cake_name}"
    

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(default=timezone.now)
    transaction_picture = models.ImageField(upload_to='transactions/', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Transaction {self.transaction_id} for Order {self.order.id}'
    
class CustomizationRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    size = models.CharField(max_length=255)
    design_details = models.TextField()
    additional_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Customization Request {self.request_id} for Order {self.order.id}'