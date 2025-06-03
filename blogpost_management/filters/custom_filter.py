import operator
from functools import reduce

import django_filters
from django.db.models import Q


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    def filter(self, queryset, value):
        # If no value is passed, just return the initial queryset
        if not value:
            return queryset
        # Return a queryset filtered for every value in the list like 'taco OR burrito OR...'
        # Change operator.or_ to operator._and to apply all filters like 'taco AND burrito AND...'
        return queryset.filter(
            reduce(operator.or_, (Q(**{f'{self.field_name}__icontains': x.strip()}) for x in value)))


class UUIDInFilter(django_filters.BaseInFilter, django_filters.UUIDFilter):
    pass