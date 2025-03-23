from django.urls import path
from apps.products.views.products import ProductView, ProductSearchView

urlpatterns = [
    path('product/<int:product_id>/', ProductView.as_view(), name='product_retrieve'),
    path('product/search/', ProductSearchView.as_view(), name='product_search'),
]
