from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'files', views.SharedFileViewSet)
router.register(r'urls', views.SharedUrlViewSet)
router.register(r'stats', views.StatView, basename='')
