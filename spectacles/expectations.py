from printer import Printer

class Expectation:

    def __init__(self, browser):
        self.printer = Printer()
        self.b = browser

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

    def assert_true(self, condition, message):

        try:
            assert condition 
            self.printer.record_pass(message)
        except AssertionError:
            self.printer.record_fail(message)

