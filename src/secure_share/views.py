# -*- coding: utf-8 -*-
import pendulum
from django.http import HttpResponse, HttpResponseGone, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django_powerbank.views.auth import AbstractAccessView, StaffRequiredMixin
from pascal_templates import ListView
from pascal_templates.views import CreateView, DetailView

from . import forms, models


class HomeView(StaffRequiredMixin, TemplateView):
    template_name = "home.html"


class SharedFileDetail(StaffRequiredMixin, DetailView):
    model = models.SharedFile


class SharedUrlDetail(StaffRequiredMixin, DetailView):
    model = models.SharedUrl


class SharedFileList(StaffRequiredMixin, ListView):
    model = models.SharedFile


class SharedUrlList(StaffRequiredMixin, ListView):
    model = models.SharedUrl


class SharedCreateBase(StaffRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SharedUrlCreate(SharedCreateBase):
    model = models.SharedUrl
    fields = ('email', 'url',)

    def get_success_url(self):
        return resolve_url("secure_share:SharedUrlDetail", self.object.pk)


class SharedFileCreate(SharedCreateBase):
    model = models.SharedFile
    fields = ('email', 'file',)

    def get_success_url(self):
        return resolve_url("secure_share:SharedFileDetail", self.object.pk)


class SharedAuthorizeBase(SingleObjectMixin, AbstractAccessView, FormView):
    form_class = forms.AuthorizationForm
    template_name = 'authorize.html'

    # noinspection PyAttributeOutsideInit
    def check_authorization(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created < pendulum.now().subtract(days=1):
            return HttpResponseGone(_("We are sorry, the link have expired."))

    def form_valid(self, form):
        if not form.check_password(self.object.secret):
            return self.form_invalid(form)
        self.object.access_counter += 1
        self.object.save()


class SharedUrlAuthorize(SharedAuthorizeBase):
    model = models.SharedUrl

    def form_valid(self, form):
        return super(SharedUrlAuthorize, self).form_valid(form) or HttpResponseRedirect(self.object.url)


class SharedFileAuthorize(SharedAuthorizeBase):
    model = models.SharedFile

    def form_valid(self, form):
        return super(SharedFileAuthorize, self).form_valid(form) or self.download()

    def download(self):
        f = self.object.file
        response = HttpResponse(f, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={}'.format(f.name)
        response['Content-Length'] = f.size
        return response
