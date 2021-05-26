from django.db import models


class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimestampedModel):
    """A blog user."""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)


class Tag(TimestampedModel):
    """A tag for the group of posts."""

    title = models.CharField(max_length=100)


class Post(TimestampedModel):
    """A blog post."""

    title = models.CharField(max_length=200)
    body = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)


class PostComment(TimestampedModel):
    """A commentary to the blog post."""

    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    response_to = models.ForeignKey(
        'PostComment', on_delete=models.SET_NULL, null=True,
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class PostLike(TimestampedModel):
    """A positive reaction to the blog post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['post', 'creator']
