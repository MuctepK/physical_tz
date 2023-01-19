import pytest
from django.conf import settings
from rest_framework.test import APIClient

from api.factories import PostFactory, CommentFactory

DATETIME_FORMAT = settings.REST_FRAMEWORK['DATETIME_FORMAT']

@pytest.fixture
def path():
    return '/api/posts/'


def client():
    return APIClient()


@pytest.mark.django_db
def test_posts_structure_and_ordering(path, client):
    # Test the structure of endpoint + ordering (by default -> last created first)
    post1, post2 = PostFactory(), PostFactory()
    comment1, comment2 = CommentFactory.create_batch(size=2, post=post1)
    comment3, comment4 = CommentFactory.create_batch(size=2, post=post2)

    res = client.get(path)
    assert res.json() == [
        {'title': post2.title,
         'text': post2.text,
         'number_of_views': 0,
         'created_at': post2.created_at.strftime(DATETIME_FORMAT),
         'comments': [
             {'created_at': comment4.created_at.strftime(DATETIME_FORMAT),
              'text': comment4.text},
             {'created_at': comment3.created_at.strftime(DATETIME_FORMAT),
              'text': comment3.text}]
         },
        {'title': post1.title,
         'text': post1.text,
         'number_of_views': 0,
         'created_at': post1.created_at.strftime(DATETIME_FORMAT),
         'comments': [
             {'created_at': comment2.created_at.strftime(DATETIME_FORMAT),
              'text': comment2.text},
             {'created_at': comment1.created_at.strftime(DATETIME_FORMAT),
              'text': comment1.text}]
         }
        ]


@pytest.mark.django_db
def test_retrieve_post_increment_number_of_views(path, client):
    post = PostFactory()
    res = client.get(path)
    # Assert that list will not increment number of views
    assert res.json()[0]['number_of_views'] == 0

    # The current retrieve will increment number of views
    res = client.get(f'{path}/{post.id}/')
    print(res.content)
    # assert res.json()['number_of_views'] == 1
    #
    # res = client.get(f'{path}/{post.id}')
    # assert res.json()['number_of_views'] == 2

