from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser

from api.filters import ProductFilter
from api.paginations import MediumPagination
from api.permissions import IsOwnerProductOrReadOnly, IsSalesmanOrReadOnly, IsAdminUserOrReadOnly, IsSalesman
from api.serializers import CategorySerializer, ListProductSerializer, DetailProductSerializer, CreateProductSerializer, \
    ProductImageSerializer, ProductAttributeSerializer, ProductSerializer, UpdateProductAttributeSerializer, \
    LoginSerializer, UserSerializer, RegisterSerializer
from core.models import Category, Product, ProductImage, ProductAttribute
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveDestroyAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly)
    pagination_class = MediumPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    search_fields = ('name',)
    ordering = ('id', 'name', 'created_at')


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly)
    lookup_field = 'id'


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = {
        'list': ListProductSerializer,
        'retrieve': DetailProductSerializer,
        'create': CreateProductSerializer,
        'update': ProductSerializer,
    }
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('name',)
    filterset_class = ProductFilter
    pagination_class = MediumPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return self.serializer_class['update']
        return self.serializer_class[self.action] 


class CreateProductImage(CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly)
    

class DetailProductImage(RetrieveDestroyAPIView):
    queryset = ProductImage
    lookup_field = 'id'
    serializer_class = ProductImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)



class CreateProductAttribute(ListCreateAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly)


class DetailProductAttribute(GenericAPIView):

    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    lookup_field = 'id'
    pagination_class = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)

    def delete(self, request, *args, **kwargs):
        product_attribute = self.get_object()
        product_attribute.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        product_attribute = self.get_object()
        serializer = UpdateProductAttributeSerializer(instance=product_attribute, data=request.data,
                                                      partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        product_attribute = self.get_object()
        serializer = self.get_serializer(instance=product_attribute)
        return Response(serializer.data)


class LoginApiView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token': token.key
            })
        return Response({'detail': 'Не существуеет пользователя либо неверный пароль.'}, status.HTTP_400_BAD_REQUEST)


class RegisterApiView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key
        })