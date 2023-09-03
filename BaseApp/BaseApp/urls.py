from django.contrib import admin
from django.urls import include, path
# from system.views import *
from django.conf import settings
from django.conf.urls.static import static
# To Serve
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('system/', include('system.urls')),
    # path('', include('neo4J.urls')),
    # path('ecommerce/', include('ecommerce.urls')),
    path('', include('elearning.urls')),
    path('media/', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/', serve, {'document_root': settings.STATIC_ROOT}),
] 
urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
