from django.db import models
import uuid

# Create your models here.
class Product(models.Model):
    id_prod = models.BigAutoField(primary_key=True)
    dci= models.CharField(max_length=100)
    dosage= models.CharField(max_length=100)
    forme= models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    def __str__(self):
        return self.dci

class Date(models.Model):
    id_date = models.BigAutoField(primary_key=True)
    date = models.DateField(unique=True, default=None)
    def __str__(self):
        return ' %s %s' % (self.id_date, self.date)

#instance of date : datetime.date(1997, 10, 19) 
class ActualSales(models.Model):
    id_actual = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product,related_name='actual', on_delete=models.CASCADE)
    date = models.ForeignKey(Date,related_name='actualsale', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('product','date')
    def __str__(self):
        return ' %s %s %s' % ( self.product ,self.quantity, self.date.date)
        
class ForecastedSales(models.Model):
    #add related_name here so product knw what to reference as a relation
    id_forcast = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product,related_name='forecast', on_delete=models.CASCADE)
    date = models.ForeignKey(Date,related_name='forecastsale', on_delete=models.CASCADE)
    model_name =  models.CharField(max_length=50, default="auto")
    horizon = models.IntegerField(default=None)
    class Meta:
        unique_together = ('model_name','date', 'horizon')
    def __str__(self):
        return ' %s %s %s %s %s ' % ( self.product, self.quantity, self.date.date, self.model_name, self.horizon)

class AdjustedSales(models.Model):
    id_adjust = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product,related_name='adjusted', on_delete=models.CASCADE)
    date = models.ForeignKey(Date,related_name='adjustedsale', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ( 'product', 'date')
    def __str__(self):
        return ' %s %s %s' % (self.product , self.quantity,self.date.date)

class MLmodel(models.Model):
    # file will be uploaded to MEDIA_ROOT / Trained/
    #must update MEDIA_ROOT in setting
    # Indiquez dans MEDIA_URL l’URL publique de base correspondant à ce répertoire.
    pickled_modele = models.FileField(blank=True, upload_to='Trained/')
