from constance import config
from icosa.models import (
    V3_CC_LICENSE_MAP,
    V3_CC_LICENSES,
    V3_TO_V4_UPGRADE_MAP,
    V4_CC_LICENSE_CHOICES,
    V4_CC_LICENSE_MAP,
    V4_CC_LICENSES,
    Asset,
    User,
)

from django import forms
from django.conf import settings
from django.forms.widgets import ClearableFileInput, EmailInput, PasswordInput
from django.utils.translation import gettext_lazy as _


class CustomImageInput(ClearableFileInput):
    clear_checkbox_label = _("Remove")
    initial_text = _("Currently")
    input_text = _("New thumbnail")
    template_name = "widgets/custom_clearable_image_input.html"


class AssetUploadForm(forms.Form):
    file = forms.FileField()


class AssetReportForm(forms.Form):
    asset_url = forms.CharField(widget=forms.widgets.HiddenInput())
    reason_for_reporting = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={"rows": 4}),
        label="Your reason for reporting this work. (Maximum length is 1,000 characters)",
    )
    contact_email = forms.CharField(
        label="The email address you can be contacted at (optional)",
        required=False,
    )


class AssetSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        license_value = self["license"].value()

        #  CC licenses are non-revokable, but are upgradeable. If the license
        # is cc but not in our current menu of options, they can upgrade and so
        # should be able to choose a different one.
        self.fields["license"].disabled = (
            self.instance.license in V4_CC_LICENSES
        )

        if (
            self.instance.license in V3_CC_LICENSES
            and license_value not in V4_CC_LICENSES
        ):
            upgrade_option = V3_TO_V4_UPGRADE_MAP[license_value]
            self.fields["license"].choices = [
                (upgrade_option, V4_CC_LICENSE_MAP[upgrade_option]),
            ] + [
                (license_value, V3_CC_LICENSE_MAP[license_value]),
            ]
        else:
            self.fields["license"].choices = (
                [
                    ("", "No license chosen"),
                ]
                + V4_CC_LICENSE_CHOICES
                + [
                    ("ALL_RIGHTS_RESERVED", "All rights reserved"),
                ]
            )

    def clean(self):
        cleaned_data = super().clean()
        license = cleaned_data.get("license")
        visibility = cleaned_data.get("visibility")
        if visibility in ["PUBLIC", "UNLISTED"] and not license:
            self.add_error("license", "Please add a CC License.")

    thumbnail = forms.FileField(required=False, widget=CustomImageInput)

    class Meta:
        model = Asset

        fields = [
            "name",
            "description",
            "visibility",
            "license",
            "thumbnail",
            "category",
        ]


class UserSettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["email_confirm"] = forms.CharField(
            required=False, widget=EmailInput
        )
        self.fields["password_current"] = forms.CharField(
            required=False, widget=PasswordInput
        )
        self.fields["password_new"] = forms.CharField(
            required=False, widget=PasswordInput
        )
        self.fields["password_confirm"] = forms.CharField(
            required=False, widget=PasswordInput
        )

    def clean(self):
        cleaned_data = super().clean()
        user = self.user

        password_current = cleaned_data.get("password_current")
        password_new = cleaned_data.get("password_new")
        password_confirm = cleaned_data.get("password_confirm")
        email = cleaned_data.get("email")
        email_confirm = cleaned_data.get("email_confirm")

        if (
            password_new or password_confirm
        ) and password_new != password_confirm:
            msg = "Passwords must match"
            self.add_error("password_new", msg)
            self.add_error("password_confirm", msg)

        if (password_new or password_confirm) and not password_current:
            msg = "Please enter your current password"
            self.add_error("password_current", msg)

        if password_new and password_confirm and password_current:
            msg = "Your current password is incorrect"
            try:
                if not user.check_password(password_current):
                    self.add_error("password_current", msg)
            except AttributeError:
                self.add_error("password_current", msg)

        if email and email != user.email:
            if email != email_confirm:
                msg = "Email addresses must match"
                self.add_error("email", msg)
                self.add_error("email_confirm", msg)

    class Meta:
        model = User

        fields = [
            "url",
            "displayname",
            "description",
            "email",
        ]


class NewUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password_new"] = forms.CharField(
            required=True, widget=PasswordInput
        )
        self.fields["password_confirm"] = forms.CharField(
            required=False, widget=PasswordInput
        )

    def clean(self):
        cleaned_data = super().clean()

        email = self.cleaned_data.get("email")
        if config.REGISTRATION_ALLOW_LIST and email not in [
            x.strip() for x in config.REGISTRATION_ALLOW_LIST.split(",")
        ]:
            msg = "New registrations are currently by invitation only. It looks like that email address is not on the invitation list."
            self.add_error("email", msg)

        password_new = cleaned_data.get("password_new")
        password_confirm = cleaned_data.get("password_confirm")

        if (
            password_new or password_confirm
        ) and password_new != password_confirm:
            msg = "Passwords must match"
            self.add_error("password_new", msg)
            self.add_error("password_confirm", msg)

    class Meta:
        model = User

        fields = [
            "url",
            "displayname",
            "email",
        ]


class PasswordResetForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            "email",
        ]


class PasswordResetConfirmForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password_new"] = forms.CharField(
            required=True, widget=PasswordInput
        )
        self.fields["password_confirm"] = forms.CharField(
            required=False, widget=PasswordInput
        )

    def clean(self):
        cleaned_data = super().clean()

        password_new = cleaned_data.get("password_new")
        password_confirm = cleaned_data.get("password_confirm")

        if (
            password_new or password_confirm
        ) and password_new != password_confirm:
            msg = "Passwords must match"
            self.add_error("password_new", msg)
            self.add_error("password_confirm", msg)

    class Meta:
        model = User
        fields = []
