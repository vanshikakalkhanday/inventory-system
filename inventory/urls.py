from django.urls import path

from . import views

urlpatterns = [

    path('', views.product_list, name='product_list'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('category/<int:id>/', views.product_by_category, name='product_by_category'),

    path('add/', views.add_product, name='add_product'),

    path('edit/<int:id>/', views.edit_product, name='edit_product'),

    path('delete/<int:id>/', views.delete_product, name='delete_product'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.view_cart, name='view_cart'),

    path('update-cart/<int:id>/', views.update_cart, name='update_cart'),

    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
 
 

]
 