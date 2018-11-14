from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    #items = models.ManyToManyField(Items,related_name='products_items')
    name = models.CharField(max_length=200,db_index=True)
    content = models.TextField(default='')
    slug = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads',blank=True)
    available = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Items(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=0)
    stock = models.PositiveIntegerField()
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Users(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=20)
    linetoken = models.CharField(max_length=150)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.username