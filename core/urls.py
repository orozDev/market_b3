from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('products/', views.main, name='products'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:id>/', views.detail_product, name='detail_product'),
]
