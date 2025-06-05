import pytz
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.response import Response
from datetime import datetime
from blogpost_management.api_exception import StandardizedException
from blogpost_management.filters.blogpost_filter import BlogPostFilter
from blogpost_management.helper_methods import notify_ws_clients, send_follow_notification
from blogpost_management.models import BlogPostModel, Comment
from blogpost_management.models.domain_model import Status
from blogpost_management.pagination import CommonPagination
from blogpost_management.serializers.blogpost_serializer import BlogPostSerializer, CommentSerializer
from user_management.models import Users
from utils.decorators import trace_log
from utils.logger import service_logger
from utils.permission import IsAuthenticatedWithSimpleToken


class BlogPostViewSet(NestedViewSetMixin, ModelViewSet):

    model = BlogPostModel
    permission_classes = [IsAuthenticatedWithSimpleToken]
    serializer_class = BlogPostSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)
    filterset_class = BlogPostFilter
    pagination_class = CommonPagination
    ordering_fields = '__all__'
    ordering = 'created_at'
    http_method_names = ['post', 'put', 'patch', 'delete', 'get']
    search_fields = ['user__firstname', 'user__lastname', 'user__email']

    def __init__(self, *args, **kwargs):
        super(BlogPostViewSet, self).__init__(*args, **kwargs)

    def get_queryset(self):
        self.queryset = BlogPostModel.objects.get_api_queryset()
        return self.queryset

    @trace_log
    def create(self, request, *args, **kwargs):
        try:
            serializer = BlogPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            notify_ws_clients('created', serializer.data)
            return Response({"success":True,"message":"Blog Post Created Successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True, error_obj=e, status_code=status.HTTP_400_BAD_REQUEST)

    @trace_log
    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = False
            obj = self.get_object()
            serializer = self.serializer_class(obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            notify_ws_clients('updated', serializer.data)
            response_data = self.serializer_class(obj).data
            return Response({"Success":True,"message":"Blog Post Updated Successfully",
                             "data":response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True,
                                        error_obj=e,
                                        status_code=status.HTTP_400_BAD_REQUEST)

    @trace_log
    def list(self, request, *args, **kwargs):
        try:
            user_id = request.query_params.get('user_id')
            queryset = BlogPostModel.objects.filter(author=user_id).exclude(status=2)
            page = self.paginate_queryset(queryset)
            serializer = BlogPostSerializer(page, many=True)
            return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True, error_obj=e, status_code=status.HTTP_400_BAD_REQUEST)

    @trace_log
    def retrieve(self, request, *args, **kwargs):
        try:
            data = BlogPostSerializer(self.get_object()).data
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True, error_obj=e, status_code=status.HTTP_400_BAD_REQUEST)

    @trace_log
    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.status_id = Status.deleted()
            obj.deleted_at = datetime.now(pytz.utc)
            obj.save()
            notify_ws_clients('deleted',obj.id)
            return Response('BlogPost deleted successfully', status=status.HTTP_200_OK)
        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True, error_obj=e, status_code=status.HTTP_400_BAD_REQUEST)



class CommentViewSet(NestedViewSetMixin, ModelViewSet):
    model = Comment
    permission_classes = [IsAuthenticatedWithSimpleToken]
    serializer_class = CommentSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)
    pagination_class = CommonPagination
    ordering_fields = '__all__'
    ordering = 'created_at'
    http_method_names = ['post', 'put', 'patch', 'delete', 'get']
    search_fields = ['user__firstname', 'user__lastname', 'user__email']

    def __init__(self, *args, **kwargs):
        super(CommentViewSet, self).__init__(*args, **kwargs)

    def get_queryset(self):
        self.queryset = Comment.objects.get_api_queryset()
        return self.queryset

    @trace_log
    def create(self, request, *args, **kwargs):
        try:

            serializer = CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            comment = serializer.save()

            notify_ws_clients('comment added', serializer.data)
            blog = BlogPostModel.objects.filter(id=request.data.get('blog_post')).first()
            post_owner = Users.objects.filter(id=str(blog.author.id)).first()
            send_follow_notification(post_owner,blog)

            response_serializer = CommentSerializer(comment)

            return Response({
                "success": True,
                "message": "Comment Added on Post Successfully",
                "data": response_serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True, error_obj=e, status_code=status.HTTP_400_BAD_REQUEST)

    @trace_log
    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = False
            obj = self.get_object()
            serializer = self.serializer_class(obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            notify_ws_clients('comment updated', serializer.data)
            response_data = self.serializer_class(obj).data
            return Response({"Success":True,"message":"Blog Post Updated Successfully",
                             "data":response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True,
                                        error_obj=e,
                                        status_code=status.HTTP_400_BAD_REQUEST)

    @trace_log
    def list(self, request, *args, **kwargs):
        try:
            blog_id = request.query_params.get('blog_id')
            user_id = request.query_params.get('user_id')
            queryset = Comment.objects.exclude(status=2)

            if blog_id:
                queryset = queryset.filter(blog_post=blog_id)
            if user_id:
                queryset = queryset.filter(user=user_id)

            page = self.paginate_queryset(queryset)
            serializer = CommentSerializer(page, many=True)
            return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True, error_obj=e, status_code=status.HTTP_400_BAD_REQUEST)

    @trace_log
    def retrieve(self, request, *args, **kwargs):
        try:
            data = CommentSerializer(self.get_object()).data
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True, error_obj=e, status_code=status.HTTP_400_BAD_REQUEST)

    @trace_log
    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.status_id = Status.deleted()
            obj.deleted_at = datetime.now(pytz.utc)
            obj.save()
            notify_ws_clients('comment deleted', obj.id)
            return Response('Comment deleted successfully', status=status.HTTP_200_OK)
        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True, error_obj=e, status_code=status.HTTP_400_BAD_REQUEST)