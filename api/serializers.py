from rest_framework import serializers

from api.models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'text')


class DetailPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'comments', 'created_at', 'number_of_views')


class ListPostSerializer(serializers.ModelSerializer):
    last_comment = CommentSerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'last_comment', 'created_at', 'number_of_views')
