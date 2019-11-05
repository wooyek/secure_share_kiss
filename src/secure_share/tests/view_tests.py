# coding=utf-8
import logging

import faker
import pendulum
import pytest
from django import test
from django.shortcuts import resolve_url
from pytest_lazyfixture import lazy_fixture

from .. import models
from . import factories, assert_no_form_errors, get_client

log = logging.getLogger(__name__)
fake = faker.Faker()

DETAIL_FACTORIES = (
    factories.SharedFileFactory,
    factories.SharedUrlFactory,
)


def get_item_create_url(factory):
    # noinspection PyProtectedMember
    model_name = factory._meta.model.__name__
    view_name = "secure_share:{}Create".format(model_name)
    return resolve_url(view_name)


def get_item_detail_url(factory):
    item = factory()
    if hasattr(item, 'get_absolute_url'):
        url = item.get_absolute_url()
    else:
        # noinspection PyProtectedMember
        model_name = factory._meta.model.__name__
        view_name = "secure_share:{}Detail".format(model_name)
        url = resolve_url(view_name, item.pk)
    log.debug("url: %s", url)
    return url


def get_model_url(factory, view_suffix):
    # noinspection PyProtectedMember
    model_name = factory._meta.model.__name__
    return resolve_url("secure_share:{}{}".format(model_name, view_suffix))


# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyProtectedMember
@pytest.mark.django_db
@pytest.mark.parametrize(
    "factory", DETAIL_FACTORIES
)
class DetailViewsTest(object):

    def test_anonymous(self, client, factory):
        url = get_item_detail_url(factory)
        response = client.get(url)
        assert 302 == response.status_code

    def test_get(self, admin_client, factory):
        url = get_item_detail_url(factory)
        response = admin_client.get(url)
        assert 200 == response.status_code


# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyProtectedMember
@pytest.mark.django_db
@pytest.mark.parametrize(
    "factory", DETAIL_FACTORIES
)
class CreateViewTest(object):

    def test_anonymous(self, factory):
        url = get_item_create_url(factory)
        response = test.Client().get(url)
        assert response.status_code == 302

    def test_forbidden(self, factory, authenticated_client):
        url = get_item_create_url(factory)
        response = authenticated_client.get(url)
        assert response.status_code == 403

    def test_get(self, factory, admin_client):
        url = get_item_create_url(factory)
        response = admin_client.get(url)
        assert response.status_code == 200


# noinspection PyUnusedLocal,PyMethodMayBeStatic,PyProtectedMember
@pytest.mark.django_db
@pytest.mark.parametrize(
    "factory", DETAIL_FACTORIES
)
class AuthorizeViewsTest(object):

    def test_anonymous(self, client, factory):
        model_name = factory._meta.model.__name__
        view_name = "secure_share:{}Authorize".format(model_name)
        item = factory()
        url = resolve_url(view_name, item.pk)
        response = client.get(url)
        assert 200 == response.status_code

    def test_bad_password(self, client, factory):
        model_name = factory._meta.model.__name__
        view_name = "secure_share:{}Authorize".format(model_name)
        item = factory()
        url = resolve_url(view_name, item.pk)
        response = client.post(url, data={'password': 'bad'})
        assert response.status_code == 200
        form = response.context_data.get('form')
        assert form.errors['password'] == ['Invalid password']

    @pytest.mark.parametrize(
        "created, status", [
            (pendulum.yesterday(), 410),
            (pendulum.now().subtract(hours=23, minutes=59), 200)
        ]
    )
    def test_gone(self, client, factory, created, status):
        model_name = factory._meta.model.__name__
        view_name = "secure_share:{}Authorize".format(model_name)
        item = factory()
        # The model field as auto_now set, so we override a `created` value directly in the db
        factory._meta.model.objects.filter(pk=item.pk).update(created=created)
        url = resolve_url(view_name, item.pk)
        response = client.get(url)
        assert response.status_code == status


# noinspection PyMethodMayBeStatic
@pytest.mark.django_db
class SharedUrlAuthorizeViewTest(object):

    def test_post(self, client):
        item = factories.SharedUrlFactory()
        url = resolve_url('secure_share:SharedUrlAuthorize', item.pk)
        response = client.post(url, data={'password': item.secret})
        assert_no_form_errors(response)
        assert response.status_code == 302
        assert response.url == item.url
        item.refresh_from_db()
        assert item.access_counter == 1
        client.post(url, data={'password': item.secret})
        item.refresh_from_db()
        assert item.access_counter == 2


@pytest.mark.django_db
class SharedFileAuthorizeViewTest(object):

    def test_post(self, client):
        item = factories.SharedFileFactory()
        url = resolve_url('secure_share:SharedFileAuthorize', item.pk)
        response = client.post(url, data={'password': item.secret})
        assert_no_form_errors(response)
        assert response.status_code == 200
        assert "attachment; filename={}".format(item.file.name) == response.get('Content-Disposition')
        assert item.file.read() == response.content


# noinspection PyMethodMayBeStatic
@pytest.mark.django_db
@pytest.mark.parametrize(
    "factory", DETAIL_FACTORIES
)
class StoreUserAgentMiddlewareTest(object):

    def test_anonymous(self, factory):
        url = get_item_create_url(factory)
        test.Client().get(url, HTTP_USER_AGENT='foo')
        assert models.UserAgent.objects.exists() is False

    def test_forbidden(self, factory, authenticated_client):
        url = get_item_create_url(factory)
        assert models.UserAgent.objects.exists() is False
        authenticated_client.get(url, HTTP_USER_AGENT='foo')
        assert models.UserAgent.objects.exists() is True

    def test_get(self, factory, admin_client):
        url = get_item_create_url(factory)
        assert models.UserAgent.objects.exists() is False
        admin_client.get(url, HTTP_USER_AGENT='foo')
        assert models.UserAgent.objects.first().agent == 'foo'
        admin_client.get(url, HTTP_USER_AGENT='bar')
        assert models.UserAgent.objects.first().agent == 'bar'
        assert models.UserAgent.objects.count() == 1

    def test_per_user(self, factory, admin_user, staff_user):
        url = get_item_create_url(factory)
        assert models.UserAgent.objects.exists() is False
        get_client(admin_user).get(url, HTTP_USER_AGENT='foo')
        get_client(staff_user).get(url, HTTP_USER_AGENT='bar')
        assert models.UserAgent.objects.filter(user=admin_user).first().agent == 'foo'
        assert models.UserAgent.objects.filter(user=staff_user).first().agent == 'bar'
        assert models.UserAgent.objects.count() == 2


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client, status', [
        (lazy_fixture('admin_client'), 200),
        (lazy_fixture('staff_client'), 200),
        (lazy_fixture('authenticated_client'), 403),
        (lazy_fixture('anonymous_client'), 302),
    ]
)
class HomeViewTest(object):
    # noinspection PyMethodMayBeStatic
    def test_get(self, client, status):
        url = resolve_url("secure_share:HomeView")
        response = client.get(url)
        assert response.status_code == status
