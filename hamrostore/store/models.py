from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.



User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=250,null=False)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=250,null=False)
    category = models.ForeignKey(Category,on_delete = models.CASCADE,blank=True,null=True)
    preview_text = models.TextField(null=False,blank=False, verbose_name="Preview text")
    description = models.TextField(null=False,blank=False)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add = True )
    image = models.ImageField(upload_to = 'images')

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'


class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username