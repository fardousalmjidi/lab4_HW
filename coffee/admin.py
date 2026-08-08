from django.contrib import admin
from .models import CoffeeItem, Order, OrderItem

# تسجيل جميع النماذج لتظهر في لوحة تحكم الأدمن
admin.site.register(CoffeeItem)
admin.site.register(Order)
admin.site.register(OrderItem)