from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from core.forms import ProductForm, ProductImageFormSet, ProductAttributeFormSet
from core.models import Product


def main(request):
    products = Product.objects.all()

    paginator = Paginator(products, 6)
    page = int(request.GET.get('page', 1))
    products = paginator.get_page(page)

    return render(request, 'index.html', {'products': products})


def detail_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'detail_product.html', {'product': product})


def create_product(request):
    product_form = ProductForm()
    product_image_form = ProductImageFormSet()
    product_attribute_form = ProductAttributeFormSet()

    return render(request, 'create_product.html', {
        'product_form': product_form,
        'product_image_form': product_image_form,
        'product_attribute_form': product_attribute_form,
    })


# Create your views here.
