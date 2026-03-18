from django.contrib import admin
from django.urls import path
from tienda import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('acercade/', views.acercade, name='acercade'),
    path('contacto/', views.contacto, name='contacto'),
]

from tienda.views import ProductoListView

path('productos/', ProductoListView.as_view(), name='productos'),

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)