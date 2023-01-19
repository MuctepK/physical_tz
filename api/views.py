from django.db.models import F
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Post


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.prefetch_related('comments').all()
    serializer_class = None

    def retrieve(self, request, *args, **kwargs):
        # Overriding retrieve to increment the number_of_views
        # Using queryset update with F() to avoid race condition
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        Post.objects.filter(id=instance.id).update(number_of_views=F('number_of_views') + 1)
        return Response(serializer.data)
