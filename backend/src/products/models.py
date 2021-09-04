from django.db import models

# Create your models here.
class Product(models.Model):
    dci= models.CharField(max_length=100)
    dosage= models.CharField(max_length=100)
    forme= models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    def __str__(self):
        return self.dci

