import django.db  # noqa: WPS301
import pytest
from python_django_orm_blog.blog import models


@pytest.mark.django_db
def test_posting():
    """Test a typical blogging scenario with comments and likes."""
    bob = models.User.objects.create(email='bob@blog.hexlet.io')
    alice = models.User.objects.create(email='alice@blog.hexlet.io')

    assert models.User.objects.count() == 2

    bobs_intro = models.Post.objects.create(
        title='Hello, World!',
        body="Hi there, I'm Bob!",
        creator=bob,
    )

    assert models.Post.objects.count() == 1

    intro = models.Tag.objects.create(title='Introduction')
    bobs_intro.tags.add(intro)

    assert intro.post_set.count() == 1

    hello_from_alice = models.PostComment.objects.create(
        body='Hi, Bob!',
        creator=alice,
        post=bobs_intro,
    )
    bobs_response = models.PostComment.objects.create(
        body='Nice to meet you, Alice!',
        creator=bob,
        post=bobs_intro,
        response_to=hello_from_alice,
    )

    assert bobs_intro.postcomment_set.count() == 2
    assert bobs_response.response_to.post_id == bobs_response.post_id

    models.PostLike.objects.create(
        post=bobs_intro,
        creator=alice,
    )
    with django.db.transaction.atomic():
        # each post can be liked by particular user only once
        with pytest.raises(django.db.utils.IntegrityError):
            models.PostLike.objects.create(
                post=bobs_intro,
                creator=alice,
            )
    assert bobs_intro.postlike_set.count() == 1
