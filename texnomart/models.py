from typing import Any

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=500,unique=True)
    slug = models.SlugField(max_length=500,unique=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(BaseModel):
    name = models.CharField(max_length=500,unique=True)
    slug = models.SlugField(max_length=500,unique=True,blank=True)
    description = models.TextField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    discount = models.IntegerField(default=0)
    is_liked = models.ManyToManyField(User, related_name='liked_products', blank=True)




    @property
    def discounted_price(self) -> Any:
        if self.discount > 0:
            return self.price * (1 - (self.discount / 100.0))
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Image(BaseModel):
    is_primary = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.name


class Comment(BaseModel):
    class Reting(models.IntegerChoices):
        One = 1
        Two = 2
        Three = 3
        Four = 4
        Five = 5

    comment = models.TextField()
    reting = models.IntegerField(choices=Reting.choices, default=Reting.One)
    slug = models.SlugField(max_length=500,unique=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.comment)
        super(Comment, self).save(*args, **kwargs)


class Key(BaseModel):
    key_name = models.CharField(max_length=500,unique=True)

    def __str__(self):
        return self.key_name


class Value(BaseModel):
    value_name = models.CharField(max_length=500,unique=True)

    def __str__(self):
        return self.value_name


class ProductAttribute(BaseModel):
    key_name = models.ForeignKey(Key,on_delete=models.CASCADE)
    value_name = models.ForeignKey(Value,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='attributes')



