#!/usr/bin/env python3
import os

import django


def create_superuser():
    django.setup(set_prefix=False)

    from django.contrib.auth.models import User
    if User.objects.exists():
        return

    setting = os.environ.get('CREATE_SUPER_USER', None)
    if setting is None:
        return

    username, email, password = setting.split(':')
    print("Creating superuser %s %s" % (username, email))
    User.objects.create_superuser(username, email, password)


if __name__ == '__main__':
    create_superuser()
