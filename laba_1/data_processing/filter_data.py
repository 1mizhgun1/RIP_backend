from ..models import Product

def filterType(engName):
    if engName == 'ALL':
        return Product.objects.all()
    return Product.objects.filter(type=engName)


def filterPrice(productList, priceMin, priceMax):
    return productList.filter(price__range=[priceMin, priceMax])