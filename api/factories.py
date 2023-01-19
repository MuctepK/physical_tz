import factory

from api.models import Comment, Post


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment
    text = factory.Sequence(lambda n: f'Text of comment #{n}')


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    title = factory.Sequence(lambda n: f'Title of post #{n}')
    text = factory.faker.Faker('sentence')

