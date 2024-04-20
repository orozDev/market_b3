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
