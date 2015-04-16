from spectacles.functionaltest import FunctionalTestCase
from spectacles.yamldriver import YAMLDriver
from splinter import Browser 

class GoogleTestCase(FunctionalTestCase):

    def setUp(self):
    	
        self.b = Browser()
        self.yaml_driver = YAMLDriver(self, self.b)

    def test_google(self):
    	self.yaml_driver.run_many("./e2etests/yaml/spec_*.yml")
        pass

    def tearDown(self):
        self.b.quit()
