from django.core.cache import cache
from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    discount = models.IntegerField(default=0)
    is_liked = models.ManyToManyField('auth.User', related_name='liked_products', blank=True)

    @property
    def discounted_price(self):
        cache_key = f'product_{self.id}_discounted_price'
        price = cache.get(cache_key)

        if price is None:
            price = self.price * (1 - (self.discount / 100.0)) if self.discount > 0 else self.price
            cache.set(cache_key, price, timeout=60 * 15)

        return price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product_{self.id}_discounted_price')

    def __str__(self):
        return self.name

