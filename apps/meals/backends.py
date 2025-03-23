from rest_framework.filters import BaseFilterBackend
from django.utils.timezone import now


class IsOwnerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class IsTodayFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        today = now().date()
        return queryset.filter(date_of_eating__date=today)
