from django.db import models
from datetime import datetime, timezone
from .resources import POSITIONS


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")


class Staff(models.Model):

    full_name = models.CharField(max_length=255)
    duty = models.CharField(max_length=2,
                            choices=POSITIONS,
                            default='CA')
    labor_contract = models.IntegerField(default=0)

    def get_last_name(self):
        return self.full_name.split()[0]


class Orders(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductsOrders')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (datetime.now(timezone.utc) - self.time_in).total_seconds() // 60


class ProductsOrders(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    in_order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount