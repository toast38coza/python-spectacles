from spectacles.functionaltest import FunctionalTestCase
from spectacles.yamldriver import YAMLDriver
from splinter import Browser
import unittest 

class GoogleTestCase(FunctionalTestCase):

    def setUp(self):
    	
        self.b = Browser()
        self.yaml_driver = YAMLDriver(self, self.b)

    @unittest.skip("..")
    def test_run_all_yaml_tests(self):
    	self.yaml_driver.run_many("./e2etests/yaml/spec_*.yml")
    	#self.yaml_driver.run_many("./e2etests/yaml/spec_example_with_include.yml")
    	pass
        
    def test_sales_tookkit(self):
    	self.yaml_driver.run_many("./e2etests/yaml/stk_*.yml")
    	#self.yaml_driver.run_many("./e2etests/yaml/include_add_vpn_from_dashboard.yml")
    	pass

    def tearDown(self):
        self.b.quit()
