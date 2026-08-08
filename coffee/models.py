from django.db import models
from django.contrib.auth.models import User

class CoffeeItem(models.Model):
    name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    roast_level = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='coffee_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.branch_name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"طلب رقم #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    coffee = models.ForeignKey(CoffeeItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.coffee.name}"