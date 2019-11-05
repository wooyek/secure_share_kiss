# coding=utf-8
# Copyright (c) 2018 Janusz Skonieczny

import logging

import pytest
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url

from . import factories

log = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
@pytest.mark.django_db
class AdminAvailableTests(object):

    def test_admin_get(self, staff_client):
        url = resolve_url("admin:index")
        response = staff_client.get(url)
        assert response.status_code == 200


# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyProtectedMember
FACTORIES = (
    factories.SharedUrlFactory,
    factories.SharedFileFactory,
    factories.UserAgentFactory,
)


# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyProtectedMember
@pytest.mark.django_db
@pytest.mark.parametrize(
    "factory", FACTORIES
)
class AdminViewsTests(object):

    def test_changelist(self, admin_client, factory):
        url = resolve_url(admin_urlname(factory._meta.model._meta, 'changelist'))
        assert admin_client.get(url).status_code == 200

    def test_change(self, admin_client, factory):
        item = factory()
        url = resolve_url(admin_urlname(factory._meta.model._meta, 'change'), item.pk)
        assert admin_client.get(url).status_code == 200

    def test_add(self, admin_client, factory):
        url = resolve_url(admin_urlname(factory._meta.model._meta, 'add'))
        assert admin_client.get(url).status_code == 200

    def test_delete(self, admin_client, factory):
        item = factory()
        url = resolve_url(admin_urlname(factory._meta.model._meta, 'delete'), item.pk)
        assert admin_client.get(url).status_code == 200
