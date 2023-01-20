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
def test_list_posts_structure_and_ordering(path, client):
    # Test the structure of endpoint + ordering (by default -> last created first)
    post1, post2 = PostFactory(), PostFactory()
    comment1, comment2 = CommentFactory.create_batch(size=2, post=post1)
    comment3, comment4 = CommentFactory.create_batch(size=2, post=post2)

    res = client.get(path)
    assert res.json() == [
        {'id': post2.id,
         'title': post2.title,
         'text': post2.text,
         'number_of_views': 0,
         'created_at': post2.created_at.strftime(DATETIME_FORMAT),
         'last_comment': {'pk': comment4.pk,
                          'text': comment4.text}
         },
        {'id': post1.id,
         'title': post1.title,
         'text': post1.text,
         'number_of_views': 0,
         'created_at': post1.created_at.strftime(DATETIME_FORMAT),
         'last_comment': {'pk': comment2.pk,
                          'text': comment2.text},
         }
        ]


@pytest.mark.django_db
def test_detail_post_structure(path, client):
    # Test the structure of detail endpoint
    post = PostFactory()
    comment1, comment2, comment3 = CommentFactory.create_batch(size=3, post=post)
    res = client.get(f'{path}{post.id}/')
    assert res.json() == {
        'id': post.id,
        'title': post.title,
        'text': post.text,
        'comments': [{'pk': comment3.pk, 'text': comment3.text},
                     {'pk': comment2.pk, 'text': comment2.text},
                     {'pk': comment1.pk, 'text': comment1.text}],
        'created_at': post.created_at.strftime(DATETIME_FORMAT),
        'number_of_views': 1}


@pytest.mark.django_db
def test_retrieve_post_increment_number_of_views(path, client):
    post = PostFactory()
    res = client.get(path)
    # Assert that list will not increment number of views
    assert res.json()[0]['number_of_views'] == 0

    # The current retrieve will increment number of views
    res = client.get(f'{path}{post.id}/')
    assert res.json()['number_of_views'] == 1

    res = client.get(f'{path}{post.id}/')
    assert res.json()['number_of_views'] == 2
