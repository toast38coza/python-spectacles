# Django Spectacles

![Django Spectacles](http://phisick.com/core/wp-content/uploads/antique-spectacles-martin-margin-1011.jpg)

![pip install django-spectacles](https://badge.fury.io/py/django-spectacles.png)


Write **end-to-end** tests in **YAML**, run them with **Python** and output your results in **Markdown**

# Installation

    pip install django-spectacles

### Quickstart

We will create a Django project for running our intergration tests. 

	python manage.py startproject e2etests .

### Setup Spectacles (you only need to do this once)

##### Add to installed apps

**In settings.py:**

    INSTALLED_APPS = (
        ...
        spectacles,
        ...
    )

##### Add TEST_DOMAIN to settings: 

`TEST_DOMAIN` defines the base_url that spectacles will run the tests against (todo it would be nice to be able to set this as an environment variable or pass it in from the command line)

	TEST_DOMAIN = 'http://google.com'

**Note:** use 'http://localhost:8081' to use Django's default test server

##### Create a test that will run all our yaml test specs:

from the directory containing `manage.py`: 

	touch e2etests/test_e2e.py
	
**test_e2e.py:**

```
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
```

This simple test will find all yaml files in the directory `./e2etests/yaml` that start with `spec_`. This means that any yaml files that we create that match this pattern will be run when we run our e2e tests.

**Notes**

* TestCase extends `FunctionalTestCase`
* We pass a glob path to find our spec yml files

#### Write tests with YAML

Here is an example test that will perform a search in Google: 

**./e2etests/yaml/spec_search_google.yml**

```
---
- scenario: Search with Google
  steps: 
  - goto: /

  - expect_elements :
    - "#lst-ib": "search input"     
  - fill_fields:
      - "#lst-ib" : "Tangent Solutions"
  - wait: 5
  - wait_for_element : "#ires"

```

(todo: documentation for available yaml commands)

#### Run tests with Python

You can now run this with: 

	python manage.py test
	

####View Results as Markdown

Spectacles is designed to create output as Markdown. Your test should create the following output:

```
##I'm feeling lucky

* Go to url: /
* ✓ Check that search input exists
* ✓ Check that [name='btnI'] exists
* Click button: 
* waiting for #archive to load
* ✓ Element has loaded: #archive
 
##Google

* Go to url: /
* ✓ Check that search input exists
* enter Tangent Solutions into field:#lst-ib
* waiting for #ires to load
* ✓ Element has loaded: #ires
```

When parsed it would look like this:

###I'm feeling lucky

* Go to url: /
* ✓ Check that search input exists
* ✓ Check that [name='btnI'] exists
* Click button: 
* waiting for #archive to load
* ✓ Element has loaded: #archive
 
###Google

* Go to url: /
* ✓ Check that search input exists
* enter Tangent Solutions into field:#lst-ib
* waiting for #ires to load
* ✓ Element has loaded: #ires

---
**TODO:**

Some improvements I would like to ship in the near future:

* Remove dependency on Django
* Print results
* Take arguments (e.g: domain, output directory, glob for yml files)
* Maybe we don't need to run this as a test?


**Note to self: deploying to pypi:**

1. Update version in setup.py
2. Upload to pypi:
		
		python setup.py sdist upload -r pypi
		
