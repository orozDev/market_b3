from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>', views.CategoryRetrieveUpdateDestroyAPIView.as_view()),

    path('products/', views.ListProduct.as_view()),
    path('products/<int:id>/', views.ProductRetrieveUpdateDestroyAPIView.as_view()),

    path('products-attributes/<int:id>/', views.DetailProductAttribute.as_view()),
    path('products-attributes/', views.CreateProductAttribute.as_view()),

    path('products-images/<int:id>/', views.DetailProductImage.as_view()),
    path('products-images/', views.CreateProductImage.as_view()),

    path('auth/login/', views.LoginApiView.as_view()),
    path('auth/register/', views.RegisterApiView.as_view()),

]