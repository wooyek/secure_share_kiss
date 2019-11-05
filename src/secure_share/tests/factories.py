# coding=utf-8
import factory
import faker
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .. import models

fake = faker.Faker()


class UserFactory(factory.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email', domain='niepodam.pl')
    username = factory.Sequence(lambda n: fake.user_name() + str(n))
    is_staff = False
    is_active = True

    class Meta:
        model = get_user_model()


class SharedFileFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    email = factory.Faker('email', domain='niepodam.pl')
    file = factory.Sequence(
        lambda x: SimpleUploadedFile(
            '{}.txt'.format(x),
            'The {} file!'.format(x).encode('ascii')
        )
    )

    class Meta:
        model = models.SharedFile


class SharedUrlFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    email = factory.Faker('email', domain='niepodam.pl')
    secret = factory.Faker('text', max_nb_chars=20)
    url = factory.Faker('uri')

    class Meta:
        model = models.SharedUrl


class UserAgentFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    agent = factory.Faker('user_agent')

    class Meta:
        model = models.UserAgent
