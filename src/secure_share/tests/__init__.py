# coding=utf-8
import logging
import os
import sys
from collections import OrderedDict

import django
from django.apps import apps
from django.conf import settings
from django.utils.functional import empty
from django.utils.timezone import is_aware, make_naive

logging.debug("settings._wrapped: %s", settings._wrapped)

# To avoid any configuration hiccups and all that boilerplate test runner settings
# just to get Django not complain about it being not configured we'll do it here
# now SimpleTestCase should work without any database setup overhead

# noinspection PyProtectedMember
if settings._wrapped is empty:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
    # noinspection PyProtectedMember
    settings._setup()

if not apps.ready:
    django.setup()

for path in sys.path:
    logging.debug("sys.path: %s", path)

from datetime import date, datetime  # noqa F402 isort:skip
from django.test import Client, TestCase  # noqa F402 isort:skip
from django.test.runner import DiscoverRunner  # noqa F402 isort:skip

# from test_plus import TestCase

from django_powerbank.testing.base import AssertionsMx  # noqa F402 isort:skip


def fake_data(*args, **kwargs):
    fields = dict(((name, name) for name in args))
    fields.update(kwargs)
    return fake_data2(fields)


def fake_data2(fields):
    from faker import Faker
    fake = Faker()
    return OrderedDict(((field, getattr(fake, kind)()) for field, kind in fields.items()))


def model_to_request_data_dict(model):
    """
    Removes fields with None value. Test client will serialize them into 'None' strings that will cause validation errors.
    """
    from django.forms import model_to_dict
    data = model_to_dict(model)
    for k, v in data.copy().items():
        if v is None:
            del data[k]
        from django_powerbank.db.models.fields import ChoicesIntEnum
        if isinstance(v, ChoicesIntEnum):
            data[k] = int(v)
        if isinstance(v, date):
            data[k] = v.isoformat()
        if isinstance(v, datetime):
            if is_aware(v):
                # ISO_INPUT_FORMATS does not conform to what isoformat returns
                data[k] = make_naive(v).isoformat().replace("T", " ")
            else:
                data[k] = v.isoformat()
    return data


def assert_no_form_errors(response, form_context_key='form'):
    if not hasattr(response, 'context_data'):
        return
    forms = response.context_data.get(form_context_key)
    if forms is None:
        return
    if not isinstance(forms, list):
        forms = [forms]
    for form in forms:
        if isinstance(form.errors, dict):
            assert form.errors == {}, form.errors
        else:
            assert form.errors == [], form.errors


def get_client(user):
    client = Client()
    client.force_login(user, settings.AUTHENTICATION_BACKENDS[0])
    return client

