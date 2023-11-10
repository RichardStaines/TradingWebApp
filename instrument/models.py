from django.db import models


class Instrument(models.Model):

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=False, blank=False)
    sedol =  models.CharField(max_length =10, unique=False)
    description = models.CharField(max_length=100, unique=False)
    price_source = models.CharField(max_length=20, unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "app_instrument"

    def __str__(self):
        return f"{self.code}"
