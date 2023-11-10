from django.db import models
from portfolio.models import Portfolio


class Cash(models.Model):

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, unique=False, blank=False)
    description = models.CharField(max_length= 100, unique=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    class Meta:
        db_table = "app_cash"
