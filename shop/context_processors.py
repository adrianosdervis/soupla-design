from .models import Product


def menu_links(request):
    links = Product.objects.all()
    return dict(links=links)
