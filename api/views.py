from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import CategorySerializer, ListProductSerializer, DetailProductSerializer, CreateProductSerializer, \
    ProductImageSerializer, ProductAttributeSerializer, ProductSerializer, UpdateProductAttributeSerializer
from core.models import Category, Product, ProductImage, ProductAttribute


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
        product = serializer.save()
        detail_serializer = DetailProductSerializer(instance=product, context={'request': request})
        return Response(detail_serializer.data, status.HTTP_201_CREATED)

    products = Product.objects.all()
    serializer = ListProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PATCH'])
def detail_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PATCH':
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        detail_serializer = DetailProductSerializer(instance=product, context={'request': request})
        return Response(detail_serializer.data)

    serializer = DetailProductSerializer(instance=product, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
def create_product_image(request):
    serializer = ProductImageSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
def detail_product_image(request, id):
    product_image = get_object_or_404(ProductImage, id=id)

    if request.method == 'DELETE':
        product_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProductImageSerializer(instance=product_image, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
def create_product_attribute(request):
    serializer = ProductAttributeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PATCH'])
def detail_product_attribute(request, id):
    product_attribute = get_object_or_404(ProductAttribute, id=id)

    if request.method == 'DELETE':
        product_attribute.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PATCH':
        serializer = UpdateProductAttributeSerializer(instance=product_attribute, data=request.data,
                                                      partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    serializer = ProductAttributeSerializer(instance=product_attribute)
    return Response(serializer.data)
