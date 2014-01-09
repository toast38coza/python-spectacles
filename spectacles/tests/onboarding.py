"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from functionaltest.functionaltestcase import FunctionalTestCase
from functionaltest.pagehelper import PageHelper
from splinter import Browser
import time

"""
Define: 

Users: 
  * New user - has never signed up
  * User - has signed up 
  * Customer - has signed up and purchased a course
"""

DEFAULT_WAIT_TIME = 10


class BrowseToCourseTest(FunctionalTestCase):
    """
    * New user arrives at CreativeColibri
    * Browses courses
    * Clicks on learn
    * lands on course browse page. There are:
      * tiles for courses 
    * clicks on a course tile  
    * lands on course landing page
    """

    def setUp(self):

        self.b = Browser()
        self.ph = PageHelper()

    def test_new_user_navigate_to_course(self):

        self.step("New user arrives at CreativeColibri")
        self.ph.load_creativecolibri_homepage(self.b)   

        self._test_cc_homepage_loaded()

        self.step("Clicks on learn")
        self.b.find_by_id("cc-learn-btn").first.click()

        self._test_course_list_page_loaded()

        self.step("Click on a course")
        self.b.find_element_by_css(".course h4 a").first.click()

        self._test_course_landing_page_loaded()
        



    def _test_cc_homepage_loaded(self):

        teach_button_exists = self.b.is_element_present_by_css("#cc-teach-btn", wait_time=10)        
        learn_button_exists = self.b.find_by_id("cc-learn-btn")

        self.assertTrue(teach_button_exists, "There is a teach button")
        self.assertTrue(learn_button_exists, "There is a learn button")

    def _test_course_list_page_loaded(self):

        courses = self.b.is_element_present_by_css(".course", wait_time=10)        

        self.assertTrue(courses, "There are tiles for active courses" )

    def _test_course_landing_page_loaded(self):

        pass
        

    def _test_course_navigation(self):

        pass


    def tearDown(self):
        self.b.quit()




        
