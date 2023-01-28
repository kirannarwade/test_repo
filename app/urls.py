from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.home, name="home"),
    path('', views.ProductView.as_view(), name="home"),
    # path('product-detail/', views.product_detail, name='product-detail'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('mobile/', views.mobile_filter, name='mobile'),
    path('mobile/<slug:data>', views.mobile_filter, name='mobiledata'),
    path('laptop/', views.laptop_filter, name='laptop'),
    path('laptop/<slug:data>', views.laptop_filter, name='laptopdata'),
    path('topwear/', views.topwear_filter, name='topwear'),
    path('bottomwear/', views.bottomwear_filter, name='bottomwear'),
    path('cart/', views.show_cart, name='show_cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('delete-cart/<int:pk>', views.delete_cart, name='delete_cart'),
    path('buy/', views.buy_now, name='buy-now'),
    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(),name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name="paymentdone"),
    path('search/', views.search, name="search"),
    path('orders-detail/<int:pk>', views.OrderDetailView.as_view(), name="order-detail")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)