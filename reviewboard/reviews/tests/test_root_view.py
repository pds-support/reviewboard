"""Unit tests for reviewboard.reviews.views.RootView."""

from __future__ import unicode_literals

from djblets.siteconfig.models import SiteConfiguration
from djblets.testing.decorators import add_fixtures

from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.testing import TestCase


class RootViewTests(TestCase):
    """Unit tests for reviewboard.reviews.views.RootView."""

    fixtures = ['test_users']

    def test_with_anonymous_with_private_access(self):
        """Testing RootView with anonymous user with anonymous access not
        allowed
        """
        siteconfig = SiteConfiguration.objects.get_current()
        siteconfig.set('auth_require_sitewide_login', True)
        siteconfig.save()

        response = self.client.get(local_site_reverse('root'))

        self.assertEqual(response['Location'],
                         'http://testserver/account/login/?next=/')

    def test_with_anonymous_with_public_access(self):
        """Testing RootView with anonymous user with anonymous access allowed
        """
        response = self.client.get(local_site_reverse('root'))

        self.assertEqual(response['Location'], 'http://testserver/r/')

    def test_with_logged_in(self):
        """Testing RootView with authenticated user"""
        self.assertTrue(self.client.login(username='doc', password='doc'))

        response = self.client.get(local_site_reverse('root'))

        self.assertEqual(response['Location'], 'http://testserver/dashboard/')

    @add_fixtures(['test_site'])
    def test_with_anonymous_with_local_site_private(self):
        """Testing RootView with anonymous user with private Local Site"""
        response = self.client.get(
            local_site_reverse('root', local_site_name=self.local_site_name))

        self.assertEqual(response['Location'],
                         'http://testserver/account/login/?next=/s/%s/'
                         % self.local_site_name)

    @add_fixtures(['test_site'])
    def test_with_anonymous_with_local_site_public(self):
        """Testing RootView with anonymous user with public Local Site"""
        local_site = self.get_local_site(name=self.local_site_name)
        local_site.public = True
        local_site.save()

        response = self.client.get(local_site_reverse('root',
                                                      local_site=local_site))

        self.assertEqual(response['Location'],
                         'http://testserver/s/%s/r/' % self.local_site_name)

    @add_fixtures(['test_site'])
    def test_with_logged_in_with_local_site(self):
        """Testing RootView with authenticated user with Local Site"""
        self.assertTrue(self.client.login(username='doc', password='doc'))

        response = self.client.get(
            local_site_reverse('root', local_site_name=self.local_site_name))

        self.assertEqual(response['Location'],
                         'http://testserver/s/%s/dashboard/'
                         % self.local_site_name)
