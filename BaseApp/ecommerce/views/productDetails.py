from ..models import *
from django.views import View

class productView(View):
    def get(self, request, uid):
        productData = product.objects.get(uid=uid)
        try:
            productPrice = variant.objects.filter(
                product=uid).order_by('-id')[0]
        except:
            productPrice = ""
        productImgs = productImg.objects.filter(
            product=productData.id).order_by('-id')
        return render(request, 'ecommerce/shop-details.html', {
            "productData": productData,
            "productPrice": productPrice,
            "productImgs": productImgs,
        })
