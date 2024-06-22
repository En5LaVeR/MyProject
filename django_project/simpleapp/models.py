from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


class Material(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='products')
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    material = models.ManyToManyField(Material, through='ProductMaterial')

    def __str__(self):
        return f'{self.name.title()}: {self.description}, {self.price} р'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()
