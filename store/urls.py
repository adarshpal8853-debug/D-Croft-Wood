from django.urls import path
from . import views

urlpatterns = [

  
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),


    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:id>/', views.increase_quantity, name='increase'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease'),

   
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    
    path('checkout/', views.checkout, name='checkout'),

    
    path('payment/', views.payment, name='payment'),
    path('upi-payment/', views.upi_payment, name='upi_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),

    path('success/', views.success, name='success'),

    
    path('myorders/', views.my_orders, name='my_orders'),

    path('profile/', views.profile, name='profile'),
]