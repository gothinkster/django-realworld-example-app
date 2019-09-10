import factory
import random
from faker import Faker
from conduit.apps.authentication.models import User
from conduit.apps.profiles.models import Profile
from conduit.apps.articles.models import Article
from django.db.models.signals import post_save

faker = Faker()

from faker.providers import BaseProvider

class Provider(BaseProvider):
    def slug_gen(self, title):
        slug = title[:5].lower() + "-" + title[5:9].lower() + "-" + str(random.randint(100, 999))
        return slug.replace(" ", "")

faker.add_provider(Provider)



@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.user_name())
    email = factory.LazyAttribute(lambda _: faker.ascii_email())
    password = faker.password(length=10, special_chars=True,
                              digits=True, upper_case=True,
                              lower_case=True)
    profile = factory.RelatedFactory('conduit.tests.factories.ProfileFactory', 'user')

@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, profile=None)
    bio = faker.text()

@factory.django.mute_signals(post_save)
class ArticleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Article

    title = faker.text()
    description = faker.text()
    body = faker.text()
    author = factory.SubFactory(ProfileFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag in extracted:
                self.tags.add(tag)




