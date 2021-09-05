from django.db import models

# Create your models here.
class Product(models.Model):
    dci= models.CharField(max_length=100)
    dosage= models.CharField(max_length=100)
    forme= models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    def __str__(self):
        return self.dci

class Date(models.Model):
    id_date = models.BigAutoField(primary_key=True)
    date = models.DateField(default=None)
    #date = models.DateField(default=None,input_formats=settings.DATE_INPUT_FORMATS)


class ForecastedSales(models.Model):
    id_forcast = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    def __str__(self):
        return '__all__'

class ActualSales(models.Model):
    id_actual = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    def __str__(self):
        return '__all__'

class AdjustedSales(models.Model):
    id_adjust = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    def __str__(self):
        return '__all__'