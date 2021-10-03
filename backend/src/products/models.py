from django.db import models

# Create your models here.
class Product(models.Model):
    id= models.CharField(max_length=400, primary_key=True, serialize=False, verbose_name='ID')
    dci= models.CharField(max_length=800)
    dosage= models.CharField(max_length=400)
    forme= models.CharField(max_length=400)
    designation = models.CharField(max_length=400)
    def __str__(self):
        return self.dci

class Date(models.Model):
    id_date = models.BigAutoField(primary_key=True)
    date = models.DateField(default=None)
    def __str__(self):
        return ' %s' % (self.date)
    #date = models.DateField(default=None,input_formats=settings.DATE_INPUT_FORMATS)
#instance of date : datetime.date(1997, 10, 19) 

class ForecastedSales(models.Model):
    id_forcast = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    def __str__(self):
        return ' %s %s' % (self.product , self.quantity)

class ActualSales(models.Model):
    id_actual = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    def __str__(self):
        return ' %s %s %s' % (self.date, self.product , self.quantity)

class AdjustedSales(models.Model):
    id_adjust = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    def __str__(self):
        return ' %s %s' % (self.product , self.quantity)

   # def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
       # return AdjustedSales.objects.create(**validated_data)

    #def update(self, instance, validated_data):
        """
        Update and return an existing `adjusted sales` instance, given the validated data.
        """
        #instance.save()