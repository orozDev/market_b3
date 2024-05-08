import base64

from django.db import transaction
from drf_extra_fields.fields import Base64ImageField

from django.core.files.base import ContentFile
from rest_framework import serializers

from account.models import User
from core.models import Category, Tag, Product, ProductImage, ProductAttribute
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ImageForProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        exclude = ('product',)


class AttributeForProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        exclude = ('product',)


class ListProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    # category = serializers.CharField(source='category.name')
    tags = TagSerializer(many=True)
    images = ImageForProductSerializer(many=True)
    attributes = AttributeForProductSerializer(many=True)
    # images2 = serializers.PrimaryKeyRelatedField(many=True, queryset=ProductImage.objects.all(), source='images')

    class Meta:
        model = Product
        exclude = ('content',)


class DetailProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    images = ImageForProductSerializer(many=True)
    attributes = AttributeForProductSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ('user',)


class AttributeForCreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        exclude = ('product',)


class CreateProductSerializer(serializers.ModelSerializer):
    attributes = AttributeForProductSerializer(many=True)
    images = serializers.ListSerializer(child=Base64ImageField(), required=False)

    class Meta:
        model = Product
        fields = '__all__'

    @transaction.atomic()
    def create(self, validated_data):
        attributes = validated_data.pop('attributes', [])
        images = validated_data.pop('images', [])

        product = super().create(validated_data)

        for attribute in attributes:
            ProductAttribute.objects.create(**attribute, product=product)

        for image in images:
            image_name = image.name
            image_file = image

            product_image = ProductImage.objects.create(product=product)
            product_image.image.save(image_name, image_file)

        return product


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'


class UpdateProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        exclude = ('product',)


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions')


class RegisterSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(validators=[validate_password])
    password2 = serializers.CharField()

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions')

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password1 != password2:
            raise serializers.ValidationError({
                'password2': ['Пароли не совпадают!']
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)