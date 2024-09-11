from django.contrib import admin
from .models import Car, Gas, Accessories


# Register your models here.
admin.site.register(Car)
admin.site.register(Gas)
admin.site.register(Accessories)