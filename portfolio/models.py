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


class PortfolioRepository:

    def __init__(self, debug=False):
        self.debug = debug

    def clear_table(self):
        Portfolio.all().delete()

    def get_portfolio(self, name):
        qs = Portfolio.objects.filter(name = name)
        return qs[0] if len(qs) > 0 else None

    def get_portfolio_list(self):
        return Portfolio.objects.all()

    def update_portfolio(self, id, updates_dict):
        rec = Portfolio.objects.get(pk=id)
        for k,v in updates_dict:
            rec[k] = v
        rec.save()

    def save_from_df(self, df, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
        rec_list = [Portfolio(name=row.Name,
                              description=row.Description,
                             ) for row in df.itertuples()]
        if self.debug:
            print(rec_list)
        Portfolio.objects.bulk_create(rec_list, batch_size=len(rec_list))

