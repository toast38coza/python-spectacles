**Current Version:** Alpha: 0.0.2

**Requirements**

* Django >= 1.6

**Links:**

 * [Pivotal Tracker Project](https://www.pivotaltracker.com/s/projects/1027510)
 * [Home Page (Github Page)](http://toast38coza.github.io/django-spectacles/)


# Installation

**Install via pip:**

    pip install -U django-spectacles

---

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
(As a preference, I like to use a naming pattern along the lines of spec_*.py for the modules containing my spec tests). Let's test the Django admin login page. 

In the folder 

#### First: write what we expect the page to do in plain text:

    * Go to /admin/
	* It has an h1 which says: "Django Administration"
	* There is a textbox for username
	* There is a textbox for password     

Now let's wrap that into a test: 


	from spectacles.functionaltest import FunctionalTestCase
	from spectacles.common import DEFAULT_WAIT_TIME, get_absolute_url as u
	from splinter import Browser 


	class HomePageTestCase(FunctionalTestCase):

   		def setUp(self):
       	    self.b = Browser()

	    def test_admin_page(self):
	        """
			* Go to /admin/
        	* It has an h1 which says: "Django Administration"
        	* There is a textbox for username
        	* There is a textbox for password        
	        """
	        self.assertTrue(False, "Not yet implemented")
	        
		def tearDown(self):
       	    self.b.quit()

**Notes:**

* We extend `FunctionalTestCase`, not `TestCase`
* `get_absolute_url` handles getting urls using the value you have set for `TEST_DOMAIN`

#### Finally: write the actual test code:

**Update `test_admin_page()` so it looks like this:**


    def test_admin_page(self):
	    """
		* Go to /admin/
        * It has an h1 which says: "Django Administration"
        * There is a textbox for username
        * There is a textbox for password        
	    """
	 

        self.scenario("Testing django-admin login page")
        self.step("Go to admin page")
        self.b.visit(u("/admin/"))

        expect = [
            ("h1", "Page heading"),            
            ("#id_username", "Username text box."),            
            ("#id_password", "Password text box."),            
        ]

        self.expect(expect)

**What this does:**

* Goes to /admin/
* Tests for an h1 and fields with the ids: id_username and id_password

**Notes:**

We are using `splinter` to wrap our selenium functionality. To see what you can do with splinter's web-drivers check out the docs at: 
http://splinter.cobrateam.info/docs/


### 3. Run your test

You can now run your spec tests using:

    python manage.py test -p spec*.py
    
You should see feedback something like below: 

<img src="http://dropbox.christo.s3.amazonaws.com/spectacles-result.png" />