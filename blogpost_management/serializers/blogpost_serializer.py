from django.db import transaction

from rest_framework import serializers

from blogpost_management.models.blogpost import BlogPostModel, Comment
from blogpost_management.models.domain_model import Status
from user_management.models.users_model import Users


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.all().exclude(status=2),
        error_messages={'does_not_exist': 'Invalid Author provided.',
                        'incorrect_type': 'Provide data in correct format.'}, required=False)
    title = serializers.CharField(max_length=255, required=True)
    body = serializers.CharField(allow_null=True, allow_blank=True, help_text="Main content of the blog post.")
    description = serializers.CharField(max_length=255, allow_null=True, allow_blank=True,required=False)
    category = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)

    @transaction.atomic
    def create(self, validated_data):
        obj = BlogPostModel.objects.create_with_defaults(**validated_data)
        return obj

    @transaction.atomic
    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = BlogPostModel
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    blog_post = serializers.PrimaryKeyRelatedField(
        queryset=BlogPostModel.objects.all().exclude(status=2),
        error_messages={'does_not_exist': 'Invalid Blog provided.',
                        'incorrect_type': 'Provide data in correct format.'}, required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all().exclude(status=2),
        error_messages={'does_not_exist': 'Invalid User provided.',
                        'incorrect_type': 'Provide data in correct format.'}, required=False)
    text = serializers.CharField(allow_null=True, allow_blank=True, help_text="Comment of the blog post.")

    @transaction.atomic
    def create(self, validated_data):
        obj = Comment.objects.create_with_defaults(**validated_data)
        return obj

    @transaction.atomic
    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = Comment
        fields = '__all__'

