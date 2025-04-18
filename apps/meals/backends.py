from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend
from django.utils.timezone import now
from django.utils.dateparse import parse_date


class IsOwnerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class MealDateFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        parsed_from_date = parse_date(from_date) if from_date else None
        parsed_to_date = parse_date(to_date) if to_date else None

        if (from_date and not parsed_from_date) or (to_date and not parsed_to_date):
            raise ValidationError('Invalid date format')
        if parsed_from_date and parsed_to_date:
            return queryset.filter(date_of_eating__date__range=(parsed_from_date, parsed_to_date))

        today = now().date()
        return queryset.filter(date_of_eating__date=today)
