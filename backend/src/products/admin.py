from django.contrib import admin
from .models import ActualSales, Date, Product
# Register your models here.
admin.site.register(Product)
admin.site.register(Date)
admin.site.register(ActualSales)