from django.db import models

TYPES = (
    ('R', 'unleaded'),
    ('M', 'Mid-grade'),
    ('P', 'Premium')
)

# Create your models here.
class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    
    def __str__(self):
     return self.make
 
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
      
class Accessories(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
     return self.name