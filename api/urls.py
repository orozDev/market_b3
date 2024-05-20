from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>', views.CategoryRetrieveUpdateDestroyAPIView.as_view()),



    path('products-attributes/<int:id>/', views.DetailProductAttribute.as_view()),
    path('products-attributes/', views.CreateProductAttribute.as_view()),

    path('products-images/<int:id>/', views.DetailProductImage.as_view()),
    path('products-images/', views.CreateProductImage.as_view()),

    path('auth/login/', views.LoginApiView.as_view()),
    path('auth/register/', views.RegisterApiView.as_view()),

    path('', include(router.urls))

]