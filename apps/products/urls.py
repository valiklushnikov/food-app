from django.urls import path
from apps.products.views.product import ProductView, ProductSearchView

urlpatterns = [
    path('product/<int:product_id>/', ProductView.as_view(), name='product_retrieve'),
    path('product/search/', ProductSearchView.as_view(), name='product_search'),
]