# Python Spectacles

For detailed documentation, [read the docs](http://spectacles.readthedocs.org)

![Django Spectacles](http://phisick.com/core/wp-content/uploads/antique-martin-margin-1011-620x480.jpg)

[![Build Status](https://travis-ci.org/toast38coza/python-spectacles.svg?branch=master)](https://travis-ci.org/toast38coza/python-spectacles)

[![Documentation Status](https://readthedocs.org/projects/spectacles/badge/?version=latest)](http://spectacles.readthedocs.io/en/latest/?badge=latest)


Write **end-to-end** tests in **YAML**, run them with **Python** and output your results in **Markdown**

# Installation

    pip install python-spectacles

# Running spectacles:

```
spectacles [OPTIONS] BASE_URL
```

e.g.: 

```
spectacles http://google.com
```

**More details on CLI and options**
```
python spectacles --help
Usage: runner.py [OPTIONS] BASE_URL

Options:
  --driver TEXT               Select the browser driver you would like to use
                              (phantomjs, chrome, firefox)
  --spec-location TEXT        A glob for finding spec files
  --out-location TEXT         path to the directory where we will output the
                              spec results
  --screenshot-location TEXT  path where we will save screenshots
  --help                      Show this message and exit.

```

### Quickstart

The default project layout is like this:

```
 .
 |_ specs/ # put your yaml specs here
 |_ reports/
     |_ screenshots # any screenshots you take will be saved here
     |_ specs # spec reports will be saved here
```

You can create that layout with the following commands:

```
mkdir specs
mkdir -p reports/screenshots
mkdir -p reports/specs
```

**Let's create a quick spec:**

`./specs/google_im_lucky.yml`

```yaml

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

```

**Run your spec:**

```
spectacles https://www.google.com
```

**Results:**

1. You should find a collection of screenshots at: `./reports/screenshots`

**Output:**

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

---

**TODO:**

Some improvements I would like to ship in the near future:

- [ ] Print results
- [ ] Generate reports
- [ ] Prompts
- [ ] Variables
- [ ] Refactor / neaten
- [ ] Improve test coverage
- [x] Remove dependency on Django
- [x] Take arguments (e.g: domain, output directory, glob for yml files)
- [x] Maybe we don't need to run this as a test?


**Note to self: deploying to pypi:**

1. Update version in setup.py
2. Upload to pypi:
		
		python setup.py sdist upload -r pypi
		
