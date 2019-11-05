# coding=utf-8
# Copyright (c) 2018 Janusz Skonieczny

import logging, sys, os, pathlib

import html2text
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

log = logging.getLogger(__name__)


def send_mail_template(template, ctx, subject, to=None, **kwargs):
    """Simplifies message rendering"""

    ctx.setdefault('BASE_URL', settings.BASE_URL)

    html_message = render_to_string(template, ctx)
    text_message = html2text.html2text(html_message)

    if not isinstance(to, list):
        to = [to]

    kwargs.setdefault('from_email', settings.DEFAULT_FROM_EMAIL)

    message = EmailMultiAlternatives(subject, body=text_message, to=to, **kwargs)
    if html_message:
        message.attach_alternative(html_message, 'text/html')
    logging.debug("to: %s", to)

    return message.send()
