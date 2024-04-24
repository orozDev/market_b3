from pprint import pprint

from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from api.serializers import CategorySerializer, ListProductSerializer, DetailProductSerializer, CreateProductSerializer
from core.models import Category, Product


@api_view(['GET', 'POST'])
def list_and_create_categories(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def detail_update_delete_category(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'PUT' or request.method == 'PATCH':
        partial = request.method == 'PATCH'
        serializer = CategorySerializer(instance=category, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = CategorySerializer(category)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def list_products(request):
    if request.method == 'POST':
        serializer = CreateProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    products = Product.objects.all()
    serializer = ListProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def detail_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = DetailProductSerializer(instance=product, context={'request': request})
    return Response(serializer.data)