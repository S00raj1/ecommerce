from django.shortcuts import render,redirect
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Sum
from .models import *
import accounts
from accounts.models import Profile
# Create your views here.


def home(request):
    
    content = {
        'title': 'home',
        'item' : Product.objects.all(),
        'category' : Category.objects.all(),
        'profile' : Profile.objects.filter(user = request.user.id),
        'page' : 'logout'
    }
   
    return render(request, 'home.html', content)
        

def about(request):
    content = {
        'title' : 'about us',
        'category' : Category.objects.all(),
        'profile' : Profile.objects.filter(user=request.user),
    }
    return render(request,'about.html',content)

def contact(request):
    content = {
        'title' : 'contact us',
        'category' : Category.objects.all(),
        'profile' : Profile.objects.filter(user=request.user),
    }
    return render(request,'contact.html',content)


class SearchResultsView(ListView):
    model = Product
    template_name = "search_results.html"
    title = 'search'
    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = Product.objects.filter(
            Q(title__icontains=query) | Q(category__title__icontains=query) 
        )
        return object_list


def detail(request,id):
    detail = Product.objects.get(id=id)

    return render(request,'detail.html',{'detail':detail,'title':'details','category' : Category.objects.all(),'profile' : Profile.objects.filter(user=request.user),})


@login_required(login_url='login')
def add_to_cart(request,id):
    item = get_object_or_404(Product,id=id)
    order_item,created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        is_active=True

    )
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.orderitems.filter(item=item).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"This item was updated.")
            return redirect ('cartview')

        else:
            order.orderitems.add(order_item)
            messages.info(request,"This item was added to your cart.")
            return redirect ('cartview')
    else:
        order = Order.objects.create(
            user = request.user)
        order.orderitems.add(order_item)
        messages.info(request,'This item was added to your cart.')
        return redirect ('cartview')

@login_required(login_url='login')
def remove_from_cart(request,id):
    item = get_object_or_404(Product,id=id)
    cart_qs = Cart.objects.filter(user=request.user, item=item, is_active=True)
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.quantity >= 1:
            cart.quantity -= 1
            cart.save()
        
        if cart.quantity <= 0:
            cart_qs.delete()
    order_qs = Order.objects.filter(
        user=request.user,
        ordered = False,
    )
    if order_qs.exists():
        order = order_qs[0]

        if order.orderitems.filter(id=id).exists():
            order_item = Cart.objects.filter(
                item = item,
                user = request.user,
            )[0]
            order.orderitems.remove(order_item)
            messages.info(request,"This item was removed from your cart.")
            return redirect('cartview')
        else:
            messages.info(request,'You do not have an active order')
            return redirect('cartview')

@login_required(login_url='login')
def cartView(request):
    # item = Cart.objects.filter(user=request.user)
    item = Cart.objects.filter(user=request.user,is_active=True).annotate(
        total = F('quantity') * F('item__price')
    )
    # total = [i.item.price*i.quantity for i in item]
    content={
        'title': 'cart',
        'item':item,
        'total' : item.aggregate(Sum('total'))['total__sum'],
        'profile' : Profile.objects.filter(user=request.user),
    }
    return render(request,'cart.html',content)

def checkout(request):
    item = Cart.objects.filter(user=request.user, is_active=True).annotate(
        total = F('quantity') * F('item__price')
    )
    order = request.user.order_set.filter(ordered=False).first()
    if request.method == 'POST':
        order.ordered = True
        order.save()
        state = request.POST['state']
        district = request.POST['district']
        city = request.POST['city']
        house = request.POST['house']
        phone = request.POST['phone']
        phone1 = request.POST['phone1']

        data = ShippingInformation.objects.create(user=request.user, order = order, state=state, district=district, city=city,house=house,phone=phone,phone1=phone1)
        data.save()
        item.update(is_active=False)
    
    content = {
        'title' : 'checkout',
        'item' : item,
        'total' : item.aggregate(Sum('total'))['total__sum'],
        'profile' : Profile.objects.filter(user=request.user),
    }
    return render(request,"checkout1.html",content)