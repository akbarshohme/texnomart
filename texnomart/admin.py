from django.contrib import admin
from texnomart.models import Category,ProductAttribute,Product,Key,Value,Image
# Register your models here.
admin.site.register(ProductAttribute)

admin.site.register(Key)
admin.site.register(Value)
admin.site.register(Image)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

