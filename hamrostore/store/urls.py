from django.urls import path
from . import views
from .views import SearchResultsView

urlpatterns = [
    path('', views.home, name="home"),
    path('category/', views.category, name="category"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('search/',SearchResultsView.as_view(),name="search"),
    path('detail/<int:id>',views.detail,name='detail'),
    path('cart/',views.add_to_cart,name="cart"),
]