from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

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


# Create your views here.
