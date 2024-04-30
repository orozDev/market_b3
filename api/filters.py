import django_filters

from core.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    price_from = django_filters.NumberFilter(lookup_expr='gte', field_name='price')
    price_to = django_filters.NumberFilter(lookup_expr='lte', field_name='price')
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['category', 'tags', 'user', 'receive_type', 'rating', 'is_published']