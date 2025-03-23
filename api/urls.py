from api.spectacular.urls import urlpatterns as doc_urls
from apps.accounts.urls import urlpatterns as account_urls
from apps.products.urls import urlpatterns as product_urls
from apps.meals.urls import urlpatterns as meal_urls


app_name = "api"

urlpatterns = []

urlpatterns += doc_urls
urlpatterns += account_urls
urlpatterns += product_urls
urlpatterns += meal_urls
