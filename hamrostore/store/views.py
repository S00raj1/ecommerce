from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from .models import *
# Create your views here.


def home(request):
    
    content = {
        'title': 'home',
        'item' : Product.objects.all(),
        'category' : Category.objects.all(),
    }
    return render(request, 'home.html', content)


def category(request):
    content = {
        'title' : 'category'
    }
    return render(request,'category.html',content)

def about(request):
    content = {
        'title' : 'about us'
    }
    return render(request,'about.html',content)

def contact(request):
    content = {
        'title' : 'contact us'
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

    return render(request,'detail.html',{'detail':detail,'title':'details'})



def add_to_cart(request):
    
    # item = get_object_or_404(Product,id=pk)
    # order_item,created = Cart.objects.get_or_create(
    #     item=item,
    #     user=request.user
    # )
    # order_qs = Order.objects.filter(user=request.user,order=False)
    # if order_qs.exists():
    #     order = order_qs[0]
    return render(request,'cart.html',{'title':'cart'})