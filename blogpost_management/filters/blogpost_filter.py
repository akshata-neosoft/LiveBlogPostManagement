import django_filters
import re

from django.db.models import Q

from .custom_filter import NumberInFilter


class BlogPostFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__category__name', lookup_expr='iexact')
    parent_question_type = django_filters.NumberFilter(field_name='parent_question_type', lookup_expr='exact')
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')
    tittle = django_filters.CharFilter(field_name='tittle', lookup_expr='icontains')