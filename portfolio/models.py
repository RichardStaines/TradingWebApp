from django.db import models


class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length= 100, unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "app_portfolio"

    def __str__(self):
        return f"{self.name}"


