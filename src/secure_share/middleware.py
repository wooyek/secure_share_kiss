import logging

from django.utils.deprecation import MiddlewareMixin

from . import models

log = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class StoreUserAgent(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_anonymous:
            return

        agent = request.META.get('HTTP_USER_AGENT', None)
        if agent is None:
            log.warning("No agent for user: {}".format(request.user.username))
            return
        agent = agent[:200]  # agent field max length
        item, created = models.UserAgent.objects.get_or_create(user=request.user, defaults={'agent': agent})
        if not created:
            item.agent = agent
            item.save()
