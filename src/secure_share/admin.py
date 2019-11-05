# coding=utf-8
from django.contrib import admin

from . import models


@admin.register(models.SharedUrl)
class SharedUrlAdmin(admin.ModelAdmin):
    list_display = ('email', 'secret', 'url')
    list_filter = ('email', 'url')
    date_hierarchy = 'created'


@admin.register(models.SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('email', 'secret', 'file')
    list_filter = ('email',)
    date_hierarchy = 'created'


@admin.register(models.UserAgent)
class UserAgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'agent',)
    list_filter = ('user', 'agent')
    date_hierarchy = 'ts'
