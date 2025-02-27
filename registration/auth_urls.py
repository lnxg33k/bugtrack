"""
URL patterns for the views included in ``django.contrib.auth``.

Including these URLs (via the ``include()`` directive) will set up the
following patterns based at whatever URL prefix they are included
under:

* User login at ``login/``.

* User logout at ``logout/``.

* The two-step password change at ``password/change/`` and
  ``password/change/done/``.

* The four-step password reset at ``password/reset/``,
  ``password/reset/confirm/``, ``password/reset/complete/`` and
  ``password/reset/done/``.

The default registration backend already has an ``include()`` for
these URLs, so under the default setup it is not necessary to manually
include these views. Other backends may or may not include them;
consult a specific backend's documentation for details.

"""

from django.conf.urls import patterns
from django.conf.urls import url
from registration.forms import (ChangePasswordForm, SetPasswordNewForm,
                                AuthForm, PasswordResetNewForm)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from django import get_version
from distutils.version import LooseVersion
from .views import updateUserProfile
from django.contrib.auth import views as auth_views

login_forbidden = user_passes_test(
  lambda u: u.is_anonymous(), reverse_lazy('profile'),
  redirect_field_name=None)

urlpatterns = patterns('',
                       url(r'^login/$',
                           login_forbidden(auth_views.login),
                           {'template_name': 'registration/login.html',
                            'authentication_form': AuthForm},
                           name='auth_login'),
                       url(r'^logout/$',
                           login_required(auth_views.logout),
                           {'next_page': reverse_lazy('profile')},
                           name='auth_logout'),
                       url(r'^password/change/$',
                           'django.contrib.auth.views.password_change',
                           {'password_change_form': ChangePasswordForm,
                            'post_change_redirect': reverse_lazy(
                                'auth_password_change_done'),
							'template_name': 'registration/password_change_form2.html'},
                           name='auth_password_change'),
                       url(r'^password/change/done/$',
                           auth_views.password_change_done,
                           name='auth_password_change_done'),
                       url(r'^password/reset/$',
                           login_forbidden(auth_views.password_reset),
                           {'post_reset_redirect': reverse_lazy(
                               'auth_password_reset_done'),
                            'password_reset_form': PasswordResetNewForm
                            },
                           name='auth_password_reset'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='auth_password_reset_complete'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='auth_password_reset_done'),
                    #    url(r'^update/$', login_required(updateUserProfile), {
                    #        'template_name': 'registration/profile_update.html'
                    #        },
                    #        name='update_profile')
                       )

if (LooseVersion(get_version()) >= LooseVersion('1.6')):
    urlpatterns += patterns('',
                            url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                                auth_views.password_reset_confirm,
                                {'post_reset_redirect': reverse_lazy(
                                    'auth_password_reset_complete'), 'set_password_form': SetPasswordNewForm, },
                                name='auth_password_reset_confirm')
                            )
else:
    urlpatterns += patterns('',
                            url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                                auth_views.password_reset_confirm,
                                {'post_reset_redirect': reverse_lazy(
                                    'auth_password_reset_complete')},
                                name='auth_password_reset_confirm')
                            )
