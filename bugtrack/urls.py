"""bugtrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
# from django.views.generic import TemplateView
from django.conf.urls.static import static

from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from app import views

login_forbidden = user_passes_test(
  lambda u: u.is_anonymous(), reverse_lazy('profile'),
  redirect_field_name=None)

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^$', login_required(views.profile), name='profile'),
    url(r'^assessment/(?P<slug>[-\w]+)$', 'app.views.view_assessment',
        name='assessment_detail'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^accounts/register/$', login_forbidden(RegistrationView.as_view(
        form_class=RegistrationFormUniqueEmail)),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^ckeditor-supersecret/', include('ckeditor.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
