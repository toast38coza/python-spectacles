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
        
        scenario_message = scenario.get("scenario")

        if not scenario_message.startswith("Partial."):
            self.testcase.scenario(scenario_message)
        
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

    def fill_fields(self, elements):

        for element in elements:
            k,v = element.items()[0]
            self.fill_field(k,v)
            
    def fill_field(self,k,v):
        exists = self.b.is_element_present_by_css(k)
        if exists:
            message = "enter {0} into field:{1}" .format (v, k)
            self.testcase.step(message)
            self.b.find_by_css(k).first.fill(v)
        else: 
            try:
                self.testcase.assertTrue(False, "Missing form field: {0}" . format(k) )
            except:
                pass
        
    def pdb(self, nothing):
        import pdb;pdb.set_trace()



    def info(self, message):
        self.testcase.info(message)

    def step(self, message):
        self.testcase.step(message)

    def todo(self, message):
        self.testcase.todo(message)

    def wait(self, seconds):
        time.sleep(seconds)

    def click(self, selector):
        button_exists = self.expect_element(selector, selector)
        button = self.b.find_by_css(selector)
        if button_exists:
            self.testcase.step("Click button: {0}" . format (button.first.text) )
            self.b.find_by_css(selector).first.click()
        else:
            self.testcase.todo("Missing button: {0}" . format(selector) )

    def select(self, selector_and_value):

        selector, value = selector_and_value.items()[0]
        el_exists = self.expect_element(selector, selector)
        if el_exists:      
            self.b.find_by_css(selector).first.select(value)
        else: 
            self.testcase.todo("Missing select: {0}" . format(selector) )

    def select_random(self, selector):
        print "select_random: TBD - selects a random option in a select"

    def check(self, selector):  
        
        el_exists = self.expect_element(selector, selector)

        if el_exists:        
            self.b.find_by_css(selector).first.check(value)
        else: 
            self.testcase.todo("Missing radio/checkbox: {0}" . format(selector) )

    def uncheck(self, selector):
        
        el_exists = self.expect_element(selector, selector)

        if el_exists:        
            self.b.find_by_css(selector).first.uncheck(value)
        else: 
            self.testcase.todo("Missing radio/checkbox: {0}" . format(selector) )

    def wait_for_element(self, selector):
        element_is_available = self.b.is_element_present_by_css(selector, wait_time=DEFAULT_WAIT_TIME)
        self.testcase.step("waiting for {0} to load" .format (selector) )
        try:
            self.testcase.assertTrue(element_is_available, "Element has loaded: {0}" . format (selector) )
        except:
            pass


    def wait_for_text(self, str):
        text_is_available = self.b.is_text_present(str, wait_time=DEFAULT_WAIT_TIME)
        self.testcase.step("waiting for text: {0}" .format (str) )
        try:
            self.testcase.assertTrue(text_is_available, "text {0} has loaded" .format (str) )
        except:
            pass
        


