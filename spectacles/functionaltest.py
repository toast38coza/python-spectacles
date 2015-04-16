#from django.test import TestCase, LiveServerTestCase
import django.dispatch
from django.conf import settings
testcase_to_extend = getattr(settings, "SPEC_TESTCASE", "LiveServerTestCase")

from django import test
import random

step_done = django.dispatch.Signal(providing_args=["testcase", "test_name" "passed"])
scenario_started = django.dispatch.Signal(providing_args=["testcase", "scenario"])


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class FunctionalTestCase(getattr(test, testcase_to_extend)):

    passed_count = 0
    failed_count = 0

    ##
    # BDD test utilities 
    ##
    def step(self, message):
        print "{0}* {1}{2}" . format (bcolors.OKBLUE, message, bcolors.ENDC)

        step_done.send(sender=self, testcase=self.__class__.__name__, test_name=self._testMethodName, passed=None)

    def todo(self, message): 
        print "{0}* **TODO:** {1}{2}" . format (bcolors.FAIL, message, bcolors.ENDC)

    def info(self, message):
        print "{0}* **INFO:** {1}{2}" . format (bcolors.OKBLUE, message, bcolors.ENDC)        

    ##
    # html testing utilities
    ##
    def expect(self, element_lookup):
        
        for selector, message in element_lookup:
            instruction = "We need an element with selector: {0}" . format(selector)
            element_exists = self.b.is_element_present_by_css(selector)
            self.assertTrue( element_exists, message, instruction )

    def expect_not(self, element_lookup):

        for selector, message in element_lookup:
            instruction = "Element: {0} - should not be on this page" . format(selector)
            element_not_exists = self.b.is_element_not_present_by_css(selector)
            self.assertTrue( element_not_exists, message, instruction )


    def fill_fields(self, field_values):
        for selector, value in field_values:
            self.b.find_by_css(selector).fill(value)

    def css(self, selector):
        return self.b.find_by_css(selector)

    def pick_random(self, elements):
         random.shuffle(elements)
         return elements.first


    ##
    # extending the default assertions 
    ##
    def assertTrue(self, assertion, description, instruction=False):
        # idea: maybe we call this: is()
        try:
            super(FunctionalTestCase, self).assertTrue(assertion)

            self.record_pass( description) 
        except:
            self.record_fail( description)

            #self.print_fail( "-> {0} is not True" . format (assertion) )         
            if instruction:
                self.todo(instruction)

        # kinda sucks to do this twice, maybe we should raise an apropriate exception?
        super(FunctionalTestCase, self).assertTrue(assertion)

    def assertEqual(self, item1, item2, description, instruction=False):
        # same .. or something?
        try:
            super(FunctionalTestCase, self).assertEqual(item1, item2)
            self.record_pass( description ) 
        except:
            self.record_fail( description)
            
            #self.print_fail( "-> {0} != {1}" . format (item1, item2) )         
            
            if instruction:
                self.todo(instruction)
        
        super(FunctionalTestCase, self).assertEqual(item1, item2)      

    ##
    # Formatting:
    ##
    def record_pass(self, message):

        self.passed_count = self.passed_count+1
        self.print_pass(message)
        step_done.send(sender=self, testcase=self.__class__.__name__, test_name=self._testMethodName, passed=True)


    def record_fail(self, message):

        self.failed_count = self.failed_count+1
        self.print_fail(message)
        step_done.send(sender=self, testcase=self.__class__.__name__, test_name=self._testMethodName, passed=False)

    def scenario(self, message):
        print " "
        print "{0}##{1}{2}\n" . format (bcolors.OKGREEN, message, bcolors.ENDC)
        scenario_started.send(sender=self, testcase=self.__class__.__name__, test_name=self._testMethodName)
        
    def print_pass(self, message):         
        print u"{0}* \u2713 {1}{2}" . format (bcolors.OKGREEN, message, bcolors.ENDC)

    def print_fail(self, message): 
        print u"{0}* \u274C {1}{2}" . format (bcolors.FAIL, message, bcolors.ENDC)
        

    def print_summary(self):

        assertion_count = float(self.failed_count + self.passed_count)
        if assertion_count > 0:
            pass_percentage = float(self.passed_count) / assertion_count * 100
        else:
            pass_percentage = "n/a"
        print "\n-"
        print "* **Failed:** {0}" . format (self.failed_count)
        print "* **Passed:** {0}" . format (self.passed_count)
        print "* **Pass Rate:** {0} %" . format ( pass_percentage )
        print "\n-"

    def tearDown(self):
        super(FunctionalTestCase, self).tearDown()

        self.print_summary()


