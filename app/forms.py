from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import string_concat
from django.core.urlresolvers import reverse_lazy
from django import forms
from app.models import Stakeholder


class StakeholderForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        username = self.initial['username']
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

# class StakeholderForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(StakeholderForm, self).__init__(*args, **kwargs)
#         # print dir(self.data)
#         # print self.base_fields
#         # print dir(self.full_clean)
#         # print self.declared_fields
#         username = self.initial['username']
#         user_id = Stakeholder.objects.get(username=username).pk
#         return user_id
#         # print user_id
#         # exit(user_id)
#         # qs = request.user.foreignkeytable__set.all()
#         # self.fields["category"].queryset = qs
#     password = ReadOnlyPasswordHashField(
#       label="Password",
#       help_text=string_concat("Raw passwords are not stored, so there is no way to see ",
#                 "this user's password, but you can change the password ",
#                 "using <a href=\"",reverse_lazy("admin:auth_user_change", args=(StakeholderForm.user_id,)),"password\">this form</a>.")
#       )
