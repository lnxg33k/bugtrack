from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import string_concat
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.forms import ModelForm
from captcha.fields import CaptchaField
from app.models import Stakeholder, Comment


class StakeholderForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        username = self.initial.get('username')
        if username:
            user_id = Stakeholder.objects.get(username=username).pk
            # print dir(x)
            # print self.auto_id
            # print dir(self)
            # print dir(self.Meta)
            self.fields['password'].help_text = string_concat("Raw passwords are not stored, so there is no way to see ",
                    "this user's password, but you can change the password ",
                    "using <a href=\"",reverse_lazy("admin:auth_user_change", args=(user_id, )),"password\">this form</a>.")

    class Meta:
        model = Stakeholder
        fields = "__all__"

    def clean_password(self):
        return ""


class CommentForm(forms.ModelForm):
    captcha = CaptchaField(required=True)

    class Meta:
        model = Comment
        # fields = "__all__"
        fields = ["comment",]
