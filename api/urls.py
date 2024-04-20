from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.list_and_create_categories),
    path('categories/<int:id>/', views.detail_update_delete_category),
    path('products/', views.list_products),
    path('products/<int:id>/', views.detail_product),
]