# coding=utf-8
# Copyright (c) 2018 Janusz Skonieczny

import logging

import pytest
from django.shortcuts import resolve_url
from mock import patch

from . import factories

log = logging.getLogger(__name__)

SHARE_FACTORIES = (
    factories.SharedFileFactory,
    factories.SharedUrlFactory,
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "factory, view_name, subject, template", (
        (factories.SharedFileFactory, 'secure_share:SharedFileAuthorize', 'foo shared a file with you', 'SharedFile/email/notification.html'),
        (factories.SharedUrlFactory, 'secure_share:SharedUrlAuthorize', 'foo shared an url with you', 'SharedUrl/email/notification.html',)
    )
)
class NotificationsTest(object):
    @patch("budget.models._send_notification")
    def send_on_create(self, factory, view_name, subject, template, _send_notification):
        factory()
        assert _send_notification.called
        assert _send_notification.call_count == 1
        item = factory(author__username='foo')
        url = resolve_url(view_name, item.pk)

        args, kwargs = _send_notification.call_args
        assert args[0] == item
        assert args[1] == subject
        assert args[2] == template
        assert args[3] == url
