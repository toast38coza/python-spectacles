from .yamldriver import YAMLDriver
import unittest, mock

class MockBrowser:
	pass


class TestInitYAMLDriver(unittest.TestCase):

	def setUp(self):
		self.browser = MockBrowser()
		options = {
			"foo": "bar",
			"spec_location": "spec_tests/*.yml"
		}
		self.base_url = "http://google.com"
		self.yamldriver = YAMLDriver(self.base_url, self.browser, options)

	def test_passed_in_values_are_set(self):
		assert self.yamldriver.foo == "bar"
		assert self.yamldriver.b == self.browser
		assert self.yamldriver.base_url == self.base_url







