# -*- coding: utf-8 -*-
from django.urls import path

from . import views as v

app_name = 'secure_share'

urlpatterns = [
    path('', v.HomeView.as_view(), name='HomeView'),

    path('file/share', v.SharedFileCreate.as_view(), name='SharedFileCreate'),
    path('file/<int:pk>/detail', v.SharedFileDetail.as_view(), name='SharedFileDetail'),
    path('file/<int:pk>/', v.SharedFileAuthorize.as_view(), name='SharedFileAuthorize'),
    path('file/', v.SharedFileList.as_view(), name='SharedFileList'),

    path('url/share', v.SharedUrlCreate.as_view(), name='SharedUrlCreate'),
    path('url/<int:pk>/detail', v.SharedUrlDetail.as_view(), name='SharedUrlDetail'),
    path('url/<int:pk>/', v.SharedUrlAuthorize.as_view(), name='SharedUrlAuthorize'),
    path('url/', v.SharedUrlList.as_view(), name='SharedUrlList'),
]
