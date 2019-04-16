from django.db import models

from conduit.apps.core.models import TimestampedModel


class Article(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)

    description = models.TextField()
    body = models.TextField()

    # Every article must have an author. This will answer questions like "Who
    # gets credit for writing this article?" and "Who can edit this article?".
    # Unlike the `User` <-> `Profile` relationship, this is a simple foreign
    # key (or one-to-many) relationship. In this case, one `Profile` can have
    # many `Article`s.
    author = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='articles'
    )

    tags = models.ManyToManyField(
        'articles.Tag', related_name='articles'
    )

    category = models.ManyToManyField(
        'articles.Category', related_name='articles'
    )

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    body = models.TextField()

    article = models.ForeignKey(
        'articles.Article', related_name='comments', on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        'profiles.Profile', related_name='comments', on_delete=models.CASCADE
    )


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag


class Category(TimestampedModel):
    """
    Here we assume that a user can create categories
    for themselves.
    """
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(db_index=True, unique=True)
    parent = models.ForeignKey(
            'self', blank=True, null=True,
            related_name='sub_categories',
            on_delete=models.CASCADE)

    class Meta:
        """
        unique_together makes sure that a category's slug isn't
        the same as that of its parent
        """
        unique_together = ('slug', 'parent',)
        verbose_name = 'categories'

    def __str__(self):
        full_path = [self.name]

        k = self.parent

        while k:
            full_path.append(k.name)
            k = k.parent
        return ' :: '.join(full_path[::-1])
