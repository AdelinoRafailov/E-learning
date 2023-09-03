from django.contrib import admin
from .models import *
# Register your models here.

#
admin.site.site_header = 'Dogs Club'


class productAdmin(admin.ModelAdmin):
    list_display = ('id','uid','name', 'description', 'category', 'active',
                    'top_product', 'created_by', 'created', 'updated',)
    search_fields = ['name', 'description', 'category__name', 'active']
    list_filter = ["category__name", "active", "top_product"]


class variantAdmin(admin.ModelAdmin):
    list_display = ('product', 'price',
                    'created_by', 'created', 'updated',)
    search_fields = ['product_name', ]
    list_filter = ["price"]

class inventoryAdmin(admin.ModelAdmin):
    list_display = ('variantref', 'quantity',
                    'created_by', 'created', 'updated',)
    search_fields = ['variantref', ]


admin.site.register(store)
admin.site.register(category)
admin.site.register(variant,variantAdmin)
admin.site.register(product, productAdmin)
admin.site.register(blog)
admin.site.register(productImg)
admin.site.register(inventory,inventoryAdmin)
admin.site.register(UserProfile)
admin.site.register(PriceHistory)
