from .models import Product
from django.db.models import Q

def search_products(request): # Изменено имя функции на search_products
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    product = Product.objects.distinct().filter(
        Q(title__icontains=search_query) # Поиск по title
        # Q(description__icontains=search_query) # Поиск по description
    )
    return product, search_query
