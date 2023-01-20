from django.db.models import F, Prefetch, Subquery, OuterRef
from django.db.models.functions import JSONObject
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Post, Comment
from api.serializers import DetailPostSerializer, ListPostSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.order_by('-created_at')

    serializer_class = DetailPostSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailPostSerializer
        return ListPostSerializer

    def retrieve(self, request, *args, **kwargs):
        # Overriding retrieve to increment the number_of_views
        # Using queryset update with F() to avoid race condition
        Post.objects.filter(id=self.kwargs.get('pk')).update(number_of_views=F('number_of_views') + 1)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'retrieve':
            qs = qs.prefetch_related(
                Prefetch('comments', queryset=Comment.objects.order_by('-created_at'))).\
                order_by('-created_at')
        else:
            qs = qs.annotate(last_comment=Subquery(
                Comment.objects.filter(post=OuterRef('pk')).order_by('-created_at')[:1]
                .values(json=JSONObject(pk='pk', text='text')))
            )
        return qs
