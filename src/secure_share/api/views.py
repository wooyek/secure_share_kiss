# coding=utf-8
# Copyright (c) 2018 Janusz Skonieczny

import logging

from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet

from .. import models
from . import serializers

log = logging.getLogger(__name__)


class SharedFileViewSet(ModelViewSet, GenericViewSet):
    queryset = models.SharedFile.objects.all()
    serializer_class = serializers.SharedFileSerializer

    def perform_create(self, serializer):
        serializer.validated_data['author_id'] = self.request.user.pk
        super(SharedFileViewSet, self).perform_create(serializer)


class SharedUrlViewSet(ModelViewSet, GenericViewSet):
    queryset = models.SharedUrl.objects.all()
    serializer_class = serializers.SharedUrlSerializer

    def perform_create(self, serializer):
        serializer.validated_data['author_id'] = self.request.user.pk
        super(SharedUrlViewSet, self).perform_create(serializer)


class StatView(ViewSet):
    """
    In addition, a secured endpoint should be created to provide information on the number of items of each type, added every day, that have been visited at least once (see example).

    Example:

    October 25, 2017, added:
        file that you have visited 5 times
        the link that has been visited 2 times

    October 26, 2017, added:
        file that has been visited 2 times
        another file that has not been visited even once
        a link that has not been visited even once
    The result of the query should be:

    {
        "2017-10-25": {
            "files": 1,
            "links": 1
        },
        "2017-10-26": {
            "files": 1,
            "links": 0
        },
    }
    """
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args, **kwargs):
        """
        Return access stats
        """
        stats = {}
        self.update_stats(stats, models.SharedUrl)
        self.update_stats(stats, models.SharedFile)
        return Response(stats)

    def update_stats(self, stats, model):
        for item in self.get_query(model):
            stats.setdefault(str(item['day']), {})['links'] = item['count']

    # noinspection PyMethodMayBeStatic
    def get_query(self, model):
        data = model.objects.filter(
            access_counter__gt=0
        ).annotate(
            day=TruncDate('created'),
            count=Count('pk'),
        ).values('day', 'count')
        return data
