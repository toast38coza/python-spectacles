from .yamldriver import YAMLDriver
import unittest, mock

class MockBrowser:
	pass


class TestInitYAMLDriver(unittest.TestCase):

	def setUp(self):
		browser = MockBrowser()
		options = {
			"foo": "bar"
			"spec_location": "spec_tests/*.yml"
		}
		base_url = "http://google.com"
		yamldriver = YAMLDriver(base_url, browser, options)

	def test_passed_in_values_are_set(self):
		assert yamldriver.foo == "bar"
		assert yamldriver.b == browser
		assert yamldriver.base_url == base_url

		





