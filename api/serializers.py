from rest_framework import serializers

from api.models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'created_at')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('title', 'text', 'comments', 'created_at', 'number_of_views')
