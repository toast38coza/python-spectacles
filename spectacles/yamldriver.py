from spectacles.common import DEFAULT_WAIT_TIME, get_absolute_url as u
import time
import yaml

class YAMLDriver:

    def __init__(self, testcase, browser):

        self.testcase = testcase
        self.b = browser

    def run(self, path_to_yaml):
        yml = yaml.load(open(path_to_yaml).read())

        scenario = yml[0]

        self.testcase.scenario(scenario.get("scenario"))
        steps = scenario.get("steps", [])

        for step in steps: 
            command, options = step.items()[0]
            method_to_call = getattr(self, command, False)

            if method_to_call:
                method_to_call(options)
            else: 
                print "No method defined for {0}" . format (command)

    def goto(self,url):
        self.testcase.step("Go to url: {0}" . format(url))
        self.b.visit(u(url))

    def expect_elements(self, elements):

        for element in elements:
            k,v = element.items()[0]
            self.expect_element(k,v)
            
    def expect_element(self,k,v):
        exists = self.b.is_element_present_by_css(k)
        message = "Check that {0} exists" .format (v)
        try:
            self.testcase.assertTrue ( exists, message )
            return True
        except:
            return False

    def info(self, message):
        self.testcase.info(message)

    def click(self, selector):
        button_exists = self.expect_element(selector, selector)
        
        if button_exists:
            self.testcase.step("Click {0}" . format (selector) )
            self.b.find_by_css(selector).first.click()
        else:
            self.testcase.todo("Missing button: {0}" . format(selector) )

    def wait_for_element(self, selector):
        element_is_available = self.b.is_element_present_by_css(selector, wait_time=DEFAULT_WAIT_TIME)
        self.testcase.step("waiting for {0} to load" .format (selector) )
        try:
            self.assertTrue(element_is_available, "Element has loaded: {0}" . format (selector) )
        except:
            pass


    def wait_for_text(self, str):
        text_is_available = self.b.is_text_present(str, wait_time=DEFAULT_WAIT_TIME)
        self.testcase.step("waiting for text: {0}" .format (str) )
        try:
            self.testcase.assertTrue(text_is_available, "text {0} has loaded" .format (str) )
        except:
            pass
        


