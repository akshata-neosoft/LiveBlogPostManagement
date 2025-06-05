from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.filters import OrderingFilter, SearchFilter
from blogpost_management.api_exception import StandardizedException
from blogpost_management.pagination import CommonPagination
from user_management.models import Users
from user_management.serializers.user_serializer import UserSerializer
from utils.decorators import trace_log

from utils.logger import service_logger
from utils.permission import IsAuthenticatedWithSimpleToken


class ProfileViewSet(NestedViewSetMixin, ModelViewSet):
    model = Users
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedWithSimpleToken]
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)
    pagination_class = CommonPagination
    ordering_fields = '__all__'
    ordering = 'created_at'
    http_method_names = ['post', 'put', 'patch', 'delete', 'get']
    search_fields = ['user__firstname', 'user__lastname', 'user__email']

    def __init__(self, *args, **kwargs):
        super(ProfileViewSet, self).__init__(*args, **kwargs)

    def get_queryset(self):
        self.queryset = Users.objects.get_api_queryset()
        return self.queryset

    @trace_log
    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = False
            obj = self.get_object()
            serializer = self.serializer_class(obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = self.serializer_class(obj).data
            return Response({"Success": True, "message": "Blog Post Updated Successfully",
                             "data": response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True,
                                        error_obj=e,
                                        status_code=status.HTTP_400_BAD_REQUEST)

    @trace_log
    def retrieve(self, request, *args, **kwargs):
        try:
            data = UserSerializer(self.get_object()).data
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True, error_obj=e, status_code=status.HTTP_400_BAD_REQUEST)

    @trace_log
    def list(self, request, *args, **kwargs):
        try:

            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            serializer = self.serializer_class(page, many=True)
            return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True, error_obj=e, status_code=status.HTTP_400_BAD_REQUEST)