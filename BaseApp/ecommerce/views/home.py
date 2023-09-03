from django.shortcuts import render
from ..models import *



def home(request):
    try:
        storeData = store.objects.all().order_by('-uid')[0]
    except:
        print("Missing details on store info")
        storeData = {}

    categoryData = category.objects.all()

    products = []
    productsData = product.objects.filter(active=True).order_by('-id')
    for i in productsData:
        try:
            record = productDetails(i)
            if record['price'] == 0:
                continue
        except Exception as e:
            print(e)
            continue
        products.append(record)

    print(len(products))

    topproductsData = product.objects.filter(top_product=True)
    blogData = blog.objects.all().order_by('-uid')

    return render(request, 'ecommerce/index.html', {
        "storeData": storeData,
        "categoryData": categoryData,
        "topproductsData": topproductsData,
        "productsData": products,
        "blogData": blogData,
    })