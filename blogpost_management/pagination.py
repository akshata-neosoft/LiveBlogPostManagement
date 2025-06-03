from rest_framework.pagination import LimitOffsetPagination

pagination_option_off = -1


"""Use this class whenever we wanted a response of the get list APIs in format of pagination response.
 when pagination is disabled response will contain data in same format as returned through paginated response."""
class CommonPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 1000
    pagination_option = None

    def paginate_queryset(self, queryset, request, view=None):
        try:
            self.pagination_option = int(request.query_params.get('pagination'))
            if self.pagination_option == pagination_option_off:
                self.default_limit = queryset.count()
        except (ValueError, TypeError):
            if isinstance(queryset, list) and self.pagination_option == pagination_option_off:
                self.default_limit = len(queryset)

        return super(CommonPagination, self).paginate_queryset(queryset, request, view)

    def get_limit(self, request):
        if self.pagination_option == pagination_option_off:
            return self.default_limit
        if request.query_params.get(self.limit_query_param, None) == '0':
            return int(request.query_params[self.limit_query_param])
        return super(CommonPagination, self).get_limit(request)

    def get_offset(self, request):
        if self.pagination_option == pagination_option_off:
            return 0

        return super(CommonPagination, self).get_offset(request)

