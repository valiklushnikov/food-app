from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]
if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
