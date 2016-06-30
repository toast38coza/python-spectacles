Getting Started
================

Installation
-------------

.. code-block:: bash

	pip install python-spectacles


Quickstart
------------


The default project layout is like this:

.. code-block:: bash

	.
	|_ specs/ # put your yaml specs here
	|_ reports/
	     |_ screenshots # any screenshots you take will be saved here
	     |_ specs # spec reports will be saved here

You can create that layout with the following commands:

.. code-block:: bash

	mkdir specs
	mkdir -p reports/screenshots
	mkdir -p reports/specs

**Let's create a quick spec:**


file: :code:`specs/im_feeling_lucky.yml`

.. code-block:: yaml

	---
	- scenario: I'm feeling lucky
	  steps: 
	  - goto: /
	  - screenshot: {}
	  - expect_elements :
	    - "#lst-ib": "search input"   
	  - fill_fields:
	    - q: "testing"
	  - wait: 1
	  - click: "[name='btnG']"
	  - wait: 5
	  - wait_for_element : "#rcnt"
	  - screenshot:
		  widths: [375, 768, 990, 1200, 1600]

**Run your spec:**

.. code-block:: bash

	spectacles https://www.google.com

**You should see a result something like the following:**

.. code-block:: markdown

	##I'm feeling lucky

	* Go to: /
	* ✓ Check that search input exists
	* enter django-spectacles into field:q
	* ✓ Check that [name='btnG'] exists
	* Click button: 
	* waiting for #rcnt to load
	* ✓ Element has loaded: #rcnt
	* Click the first link
	* ✓ Check that h3.r a exists
	* Click button: GitHub - toast38coza/django-spectacles: Write Integration tests in ...

Next Steps
-----------

Using includes
~~~~~~~~~~~~~~~~~~~~~~

There are a lot of things that you might want to do repeatedly. It doesn't make sense to have to rewrite these the whole time. That's where the `include` command comes in. 

**Create a new folder inside specs:**

.. code-block: bash

	mkdir specs/includes

Now you can create some sub-specs in "code:`specs/includes`. You can then include them from a top-level spec like so: 

.. code-block:: yaml

	---
	- scenario: Do some stuff
	  steps:
	    - include: specs/includes/login.yml
	    - include: specs/includes/do-something.yml
	    - include: specs/includes/do-something-else.yml

.. note:: by default spectacles will look for specs with the following glob :code:`specs/*.yml`. Therefore the specs in includes won't be run by the spec runner by default, but they can be included with the include directive

.. note:: the include path is relative to the location from which spectacles is being run.


