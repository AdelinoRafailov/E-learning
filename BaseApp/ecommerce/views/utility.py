from ..models import *

def getLatestPrice(productId):
    return variant.objects.filter(product=productId).order_by('-id')[0]


def getInventory(productId):

    Variants = variant.objects.filter(product=productId.id)
    Inventory = 0
    for variantLine in Variants:
        Inventory += inventory.objects.get(variantref=variantLine.id).quantity
    
    return Inventory


def productDetails(ProductId):
    record = {}
    record['id'] = ProductId.id
    record['uid'] = ProductId.uid
    record['name'] = ProductId.name
    record['description'] = ProductId.description
    record['category'] = ProductId.category
    record['weight'] = ProductId.weight
    record['img'] = ProductId.img
    record['price'] = getLatestPrice(ProductId.id).price
    record['priceid'] = getLatestPrice(ProductId.id).id
    record['inventory'] = getInventory(ProductId)
    print(record['inventory'],record['name'])

    return record
