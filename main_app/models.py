from django.db import models
from datetime import date
from django.contrib.auth.models import User

TYPES = (
    ('R', 'unleaded'),
    ('M', 'Mid-grade'),
    ('P', 'Premium')
)

# Create your models here.

class Accessories(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
     return self.name
   
   
class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    Accessories = models.ManyToManyField(Accessories)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def filled_up_today(self):
        return self.gas_set.filter(date=date.today()).count() >= len(TYPES)
 
class Gas(models.Model):
    date = models.DateField('Gas Up Date')
    type = models.CharField(max_length=1,
    choices=TYPES,
    default=TYPES[0][0]
  )
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  
    
    def __str__(self):
     return f"{self.get_type_display()} on {self.date}"
    class Meta:
      ordering = ['-date']
      verbose_name_plural = "gas"
