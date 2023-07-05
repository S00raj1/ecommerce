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
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'


    def get_total(self):
        return self.item.price * self.quantity
    
    def price_total(self):
        total = 1
        return self.total + get_total
    
    class Meta:
        ordering = ('id',)

class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total()

        return total

class ShippingInformation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
    state = models.CharField(max_length=250,null=False,blank=False)
    district = models.CharField(max_length=250,null=False,blank=False)
    city = models.CharField(max_length=250,null=False,blank=False)
    house = models.CharField(max_length=250,null=True,blank=True)
    phone = models.CharField(max_length=250,null=False,blank=False)
    phone1 = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        return self.user.username