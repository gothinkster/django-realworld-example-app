from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from conduit.apps.core.utils import generate_random_string

from .models import Article

@receiver(pre_save, sender=Article)
def add_slug_to_article_if_not_exists(sender, instance, *args, **kwargs):
    MAXIMUM_SLUG_LENGTH = 255

    if instance and not instance.slug:
        slug = slugify(instance.title)
        unique = generate_random_string()

        if len(slug) > MAXIMUM_SLUG_LENGTH:
            slug = slug[:MAXIMUM_SLUG_LENGTH]

        while len(slug + '-' + unique) > MAXIMUM_SLUG_LENGTH:
            parts = slug.split('-')

            if len(parts) is 1:
                # The slug has no hypens. To append the unique string we must
                # arbitrarly remove `len(unique)` characters from the end of
                # `slug`. Subtract one to account for extra hyphen.
                slug = slug[:MAXIMUM_SLUG_LENGTH - len(unique) - 1]
            else:
                slug = '-'.join(parts[:-1])

        instance.slug = slug + '-' + unique
