# Requirements 

* Django >= 1.6

# Installation

    ...

# Getting Started 

### 1. Add to installed apps

**In settings.py:**

    INSTALLED_APPS = (
        ...
        spectacles,
        ...
    )
    
You also need to set a value for `TEST_DOMAIN` in `settings.py`. 

	# this is the default used by Django's test server
	TEST_DOMAIN = 'http://localhost:8081'



   
### 2. Write your first functional test: 

Create a file called specs.py 
(As a preference, I like to use a naming pattern along the lines of spec_*.py for the modules containing my spec tests).

#### First: write what you want to do in plain text:

	from spectacles.functionaltest import FunctionalTestCase
	from spectacles.common import DEFAULT_WAIT_TIME, get_absolute_url as u
	from splinter import Browser 


	class HomePageTestCase(FunctionalTestCase):

   		def setUp(self):
       	self.b = Browser()

	    def test_homepage_loads(self):
	        """
			* Go to the homepage
        	* It has a h1 title        
	        """
	        
		def tearDown(self):
       	self.b.quit()

**Notes:**

* We extend `FunctionalTestCase`, not `TestCase`
* `get_absolute_url` handles getting urls using Django's LiveTestSever

#### Finally: write the actual test code:

**Add the following to `test_homepage_loads()`:**

    self.scenario("Testing loading the homepage")
    self.step("Go to homepage")
    self.b.visit(u("/"))

    expect = [
        ("h1", "There is a h1 title"),            
    ]

    self.expect(expect)


### 3. Run your test

You can now run your spec tests using:

    python manage.py test -p spec*.py
    
Assuming we haven't got an h1 on out page, we should get something like:

##Testing loading the homepage

* Go to homepage
* [x] Failed: There is a h1 title
* -> False is not True
* **TODO:** We need an element with selector: h1

A successful response should look something like:

##Testing loading the homepage

* Go to homepage
* (: Passed: There is a h1 title
.

----------------------------------------------------------------------
Ran 1 test in 19.513s

OK




