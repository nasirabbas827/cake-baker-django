from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login'),
    path('dashboard/', login_required(views.dashboard), name='dashboard'), 
    path('update_profile/', login_required(views.update_profile), name='update_profile'),
    path('change_password/', login_required(views.change_password), name='change_password'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('add_to_cart/<int:cake_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),  # Update cart item quantity
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item from cart
    path('make_order/', views.make_order, name='make_order'),
    path('order_success/', views.order_success, name='order_success'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('view_order_details/<int:order_id>/', views.view_order_details, name='view_order_details'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('orders/pay/<int:order_id>/', views.pay_order, name='pay_order'),
    path('orders/customization/<int:order_id>/', views.customization_request, name='customization_request'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
