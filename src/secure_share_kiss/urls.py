"""secure_share_kiss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import PasswordResetView
from django.urls import path, include

from secure_share.api.urls import router
from secure_share_kiss import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/password_reset/', PasswordResetView.as_view(), name='admin_password_reset'),

    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),

    path('', include('secure_share.urls')),
]

if settings.MEDIA_SERVED:
    from django.views.static import serve

    urlpatterns += [
        path('media/<path:path>', serve, kwargs={'document_root': settings.MEDIA_ROOT}),
    ]
