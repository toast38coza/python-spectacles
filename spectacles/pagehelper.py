from django.conf import settings

class PageHelper:

    def __init__(self):
        self.base_url = settings.FUNCTIONAL_TEST_BASE_URL

    def load_creativecolibri_homepage(self, b):
        b.visit(self._get_absolute_url(""))
    

    def load_course_browse_page(self, b):
        b.visit(self._get_absolute_url("/course/learn/"))

    def _get_absolute_url(self, path):

        return "{0}{1}" . format ( self.base_url, path )

