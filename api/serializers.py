from mimetypes import guess_extension
import base64

from django.core.files import File
from django.core.files.base import ContentFile
from rest_framework import serializers

from core.models import Category, Tag, Product, ProductImage, ProductAttribute


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


class AttributeForCreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        exclude = ('product',)


class CreateProductSerializer(serializers.ModelSerializer):
    attributes = AttributeForProductSerializer(many=True)
    images = serializers.ListSerializer(child=serializers.CharField(), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        attributes = validated_data.pop('attributes', [])
        images = validated_data.pop('images', [])
        name = validated_data.get('name', 'product_name')

        product = super().create(validated_data)

        for attribute in attributes:
            ProductAttribute.objects.create(**attribute, product=product)

        for image in images:
            idx = images.index(image)

            format, imgstr = image.split(';base64,')
            format_image = format.split('/')[-1]

            image_file = base64.b64decode(image)
            image_file = ContentFile(image_file)

            image_name = f'{name}_{idx}.{format_image}'
            print(image_name, image_file)

            product_image = ProductImage.objects.create(product=product)
            product_image.image.save(image_name, image_file, save=True)

        return product

