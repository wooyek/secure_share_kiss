# coding=utf-8
# Copyright (c) 2018 Janusz Skonieczny

import logging

import django.test
import pytest
from django.conf import settings

from .factories import UserFactory

log = logging.getLogger(__name__)


@pytest.fixture
def anonymous_client(staff_user):
    return django.test.Client()


@pytest.fixture
def staff_user():
    return UserFactory.create(is_superuser=False, is_staff=True)


@pytest.fixture
def staff_client(staff_user):
    client = django.test.Client()
    client.force_login(staff_user, settings.AUTHENTICATION_BACKENDS[0])
    return client


@pytest.fixture
def authenticated_client(user=None):
    user = user or UserFactory.create(is_superuser=False, is_staff=False)
    client = django.test.Client()
    client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])
    return client


@pytest.fixture
def deactivate_locale():
    from django.utils import translation
    # noinspection PyAttributeOutsideInit
    locale = translation.get_language()
    translation.deactivate_all()
    yield locale
    if locale:
        translation.activate(locale)
