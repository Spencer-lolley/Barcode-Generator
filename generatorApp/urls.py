from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='homepage'),
    path('generate/',views.create_product, name='generate_product'),
    path('product_list/', views.product_list, name='product_list'),
    # path('download/<str:barcode_path>/', BarcodeDownloadView.as_view(), name='download_barcode'),
    path('download/<path:barcode_path>/', views.download_barcode, name='download_barcode'),
]
    

