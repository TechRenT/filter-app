from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Filter


class FilterModelTests(TestCase):
    def test_filter_creation(self):
        filter1 = Filter.objects.create(
            keyword = "directory"
        )
        filter2 = Filter.objects.create(
            keyword = "google"
        )
        filter3 = Filter.objects.create(
            keyword = "yahoo"
        )
        for x in range(1, 31):
            Filter.objects.create(
                keyword = "bad_keyword{}".format(x)
            )
        now = timezone.now()
        self.assertLess(filter1.created_at, now)


class FilterViewsTest(TestCase):
    def setUp(self):
        self.filter1 = Filter.objects.create(
            keyword = "directory"
        )
        self.filter2 = Filter.objects.create(
            keyword = "google"
        )
        self.filter3 = Filter.objects.create(
            keyword = "yahoo"
        )
    def test_keywords_list_view(self):
        resp = self.client.get(reverse('filter:keywords'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.filter1, resp.context['keywords'])
        self.assertIn(self.filter2, resp.context['keywords'])
        self.assertIn(self.filter3, resp.context['keywords'])
        self.assertTemplateUsed(resp, 'filters/keywords_list.html')
        self.assertContains(resp, self.filter1)

    def test_upload_file_view(self):
        resp = self.client.get(reverse('filter:main_app'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'filters/upload.html')
