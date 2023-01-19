from django.db.models import F, Prefetch
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Post, Comment
from api.serializers import PostSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Post.objects.
        prefetch_related(
            Prefetch('comments', queryset=Comment.objects.order_by('-created_at'))).order_by('-created_at')
    )

    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        # Overriding retrieve to increment the number_of_views
        # Using queryset update with F() to avoid race condition
        Post.objects.filter(id=self.kwargs.get('pk')).update(number_of_views=F('number_of_views') + 1)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
