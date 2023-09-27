from ..models import OpticItem

def filterType(engName):
    if engName == 'ALL':
        return OpticItem.objects.all().filter(status='A')
    return OpticItem.objects.filter(type=engName).filter(status='A')


def filterPrice(productList, priceMin, priceMax):
    return productList.filter(price__range=[priceMin, priceMax])