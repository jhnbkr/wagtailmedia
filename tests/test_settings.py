from django.test import TestCase, override_settings

import mock

from wagtailmedia.settings import WagtailMediaSettings, wagtailmedia_settings


class SettingsTests(TestCase):
    def test_compatibility_with_override_settings(self):
        self.assertEqual(
            wagtailmedia_settings.MEDIA_MODEL,
            "wagtailmedia.Media",
            "Checking a known default",
        )

        with override_settings(WAGTAILMEDIA={"MEDIA_MODEL": "myapp.CustomMedia"}):
            self.assertEqual(
                wagtailmedia_settings.MEDIA_MODEL,
                "myapp.CustomMedia",
                "Setting should have been updated",
            )

        self.assertEqual(
            wagtailmedia_settings.MEDIA_MODEL,
            "wagtailmedia.Media",
            "Setting should have been restored",
        )

    def test_warning_raised_on_deprecated_setting(self):
        """
        Make sure user is alerted with an deprecated setting is used.
        """
        msg = (
            "The 'WAGTAILMEDIA_MEDIA_MODEL' setting is deprecated and will be removed in the next release, "
            'use WAGTAILMEDIA["MEDIA_MODEL"] instead.'
        )
        with self.assertWarnsMessage(PendingDeprecationWarning, msg):
            WagtailMediaSettings({"WAGTAILMEDIA_MEDIA_MODEL": "myapp.CustomMedia"})

    @mock.patch("wagtailmedia.settings.REMOVED_SETTINGS", ["A_REMOVED_SETTING"])
    def test_runtimeerror_raised_on_removed_setting(self):
        msg = (
            "The 'A_REMOVED_SETTING' setting has been removed. "
            "Please refer to the wagtailmedia documentation for available settings."
        )
        with self.assertRaisesMessage(RuntimeError, msg):
            WagtailMediaSettings({"A_REMOVED_SETTING": "myapp.CustomMedia"})
