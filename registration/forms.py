"""
Forms and validation code for user registration.

Note that all of these forms assume Django's bundle default ``User``
model; since it's not possible for a form to anticipate in advance the
needs of custom user models, you will need to write your own forms if
you're using a custom model.

"""
from __future__ import unicode_literals


from django import forms
from django.utils.translation import ugettext_lazy as _
from passwords.fields import PasswordField
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm, AuthenticationForm, PasswordResetForm, UserChangeForm

from .users import UserModel, UsernameField

User = UserModel()


class PasswordResetNewForm(PasswordResetForm):
    captcha = CaptchaField()


class UpdateProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )

    def clean_password(self):
        return ""

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']).exclude(username=self.cleaned_data['username']).count():
            raise forms.ValidationError(
                _("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class AuthForm(AuthenticationForm):
    captcha = CaptchaField()


class SetPasswordNewForm(SetPasswordForm):
    new_password1 = PasswordField(
        label="New password", help_text='Must be 8 characters or more and common sequence of characters')


class ChangePasswordForm(PasswordChangeForm):
    captcha = CaptchaField()
    new_password1 = PasswordField(
        label="New password", help_text='Must be 8 characters or more and common sequence of characters')


class RegistrationForm(UserCreationForm):

    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    required_css_class = 'required'
    captcha = CaptchaField()
    password1 = PasswordField(
        label="Password", help_text='Must be 8 characters or more and common sequence of characters')
    email = forms.EmailField(label=_("E-mail"))
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = (UsernameField(), "email", "first_name", "last_name")


class RegistrationFormTermsOfService(RegistrationForm):

    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.

    """
    tos = forms.BooleanField(widget=forms.CheckboxInput,
                             label=_(
                                 'I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms to register")})


class RegistrationFormUniqueEmail(RegistrationForm):

    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.

    """

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(RegistrationForm):

    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.

    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.

    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']

    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.

        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(
                _("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']
