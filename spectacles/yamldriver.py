import time, glob, yaml, random, requests
from .printer import Printer
from .expectations import Expectation
from splinter.request_handler.status_code import HttpResponseError

class YAMLDriver:

    wait_time = 5
    screenshot_location = './report/screenshots'

    def __init__(self, base_url, browser, options, wait_time=5):

        for key, value in options.items():
            setattr(self, key, value)

        self.base_url = base_url
        self.b = browser

        self.printer = Printer()        
        self.expectation = Expectation(self.b)
    
    def __add_trailing_slash(self, baseurl):

        if baseurl[-1] != "/":
            baseurl = "{0}/".format(baseurl)
        return baseurl

    def __url(self, path):

        if path.startswith("/"):
            path = path[1:]

        baseurl = self.__add_trailing_slash(self.base_url)
        return "{0}{1}" . format (baseurl, path)


    def run_many(self, glob_pattern):

        paths = glob.glob(glob_pattern)                
        for path in paths:            
            self.run(path)

    def run(self, path_to_yaml):        

        yml = yaml.load(open(path_to_yaml).read())
        scenario = yml[0]
        scenario_message = scenario.get("scenario")

        if not scenario_message.startswith("Partial."):
            self.printer.scenario(scenario_message)
        
        steps = scenario.get("steps", [])

        for step in steps: 
            command, options = step.items()[0]
            method_to_call = getattr(self, command, False)

            if method_to_call:                
                method_to_call(options)
            else: 
                print ("No method defined for {0}" . format (command))

    ## todo: extract to interactions class

    def include(self, path_to_include):
        '''
        Include a yaml spec. 
        
        .. note:: Path is relative to directory from which tests are being run


        **Example:**

        .. code-block:: yaml

            - include: ./path/to/file

        todo: would be nice if we could make path relative to yml file
        '''
        self.run(path_to_include)

    def goto(self, path):
        """
        Browse to a url.

        Example::
        
        .. code-block:: yaml

            # go to a single page
            goto: /path/to/page

        """

        try:
            self.b.visit(self.__url(path))
            self.printer.record_pass("Successfully visited {}" . format (path))
        except HttpResponseError as e:
            self.printer.record_pass("Error loading page: {}. {}:{}" . format (path, e.status_code, e.reason))

    def goto_pages(self, options):
        """
        Go to a list of pages. Optionally also take a screenshot
        

        **Example**
        
        .. code-block:: yaml
            
            # visit a couple of pages
            goto_pages: 
              pages:
                - /page1
                - /page2
                - /page3

            # you can also have it take a screenshot on those pages
            goto_pages: 
              pages:
                - /page1
                - /page2
                - /page3
              with_screenshot: yes
              screenshot_widths: [375, 768, 990, 1200, 1600]

        """

        pages = options.get('pages', [])
        with_screenshot = options.get('with_screenshot', None)
        screenshot_widths = options.get('screenshot_widths', None)

        for page in pages:
            self.goto(page)

            if with_screenshot:
                screen_options = {
                    "widths": screenshot_widths
                }
                self.screenshot(screen_options)

    ## TODO:
    def check_links(self, options):
        """
        Checks all the links on the current page. Verifies that they're 200 OK

        **Parameters**

        +-----------+----------+---------+-----------------------------------------------------------------------------------------------------------------------+
        | Name      | Required | Default | Description                                                                                                           |
        |-----------|----------|---------|-----------------------------------------------------------------------------------------------------------------------|
        | container | no       | None    | Specify a bounding container in which we should look for links. Useful for excluding common items like nav and footer |
        +-----------+----------+---------+-----------------------------------------------------------------------------------------------------------------------+

        **Examples:**

        .. code-block:: yaml

            # basic usage:
            - check_links: {}

            # optionally: you can specify a bounding container to look in.
            - check_links:
                container: #content

        """
        links = self.b.find_by_tag("a")
        for link in links:
            href = link._element.get_attribute('href')

            if href is not None:
                response = requests.get(href)
                message = "{}: [{}]({})" . format(response.status_code, link.text, href)
                if response.status_code == 200:
                    self.printer.record_pass(message)
                else:
                    self.printer.record_fail(message)


    def expect_values(self, elements):
        
        print ("TBD")
        """
        for element in elements:
            k,v = element.items()[0]   
            exists = self.b.is_element_present_by_css(k)
            
            if exists:    
                el = self.b.find_by_css(k).first
                self.printer.assertEqual(el.value, v)
        """

    def expect_text(self, text):
        """
        Expect text to be on the page

        **Parameters:**

        +------+----------+----------------------------------------+
        | Name | Required | Description                            |
        +------+----------+----------------------------------------+
        | text | yes      | The text we expect to find on the page |
        +------+----------+----------------------------------------+

        **Examples:**

        .. code-block:: yaml

            - expect_text: "The user details you entered are incorrect"   
        
        **Example output**

        * Found text: `The user details you entered are incorrect`

        """

        if self.b.is_text_present(text):
            self.printer.record_pass("Found text: '{}'" . format (text))
        else:
            self.printer.record_fail("Expected text: '{}'" . format (text))


    def expect_elements(self, elements):
        '''
        Example::

          - expect_elements :
            - "#lst-ib": "search input" 

        This wraps `expect_element`
        '''

        for element in elements:
            k,v = element.items()[0]
            self.expect_element(k,v)
            
    def expect_element(self,k,v):
        """
        Expect elements to exist on the page. 

        **Parameters:**

        * key: css selector
        * value: description of the field we're looking for

        Example::

            - expect_elements :
              - "#lst-ib": "search input"   

        Will output::

            "Check that search input exists"

        """

        message = "Check that {0} exists" .format (v)
        exists = self.b.is_element_present_by_css(k)
        
        try:
            assert exists 
            self.printer.record_pass(message)
            return True
        except AssertionError:
            self.printer.record_fail(message)
        return False 

    def fill_fields(self, elements):
        """
        Fill the fields on a form. 
        Takes a dictionary of key/values. Where key is the name 
        of the form input to set the value in

        Example::

            - fill_fields:
                username: joe
                password: supersecret
        """        
        for element in elements:
            k,v = element.items()[0]            
            self.fill_field(k,v)
            
    def fill_field(self,k,v):
        """
        Fill a single field. 

        Example::

            - fill_field:
                key: value
        """
    
        message = "enter {0} into field:{1}" .format (v, k)
        self.printer.step(message)
        #self.b.find_by_css(k).first.fill(v)
        self.b.type(k,v)
        
            
    def pdb(self, nothing):
        """
        Insert a pdb so you can debug what's going on.

        Example::

            - pdb: nothing

        the value doesn't really matter, but yml requires a value
        """
        import pdb;pdb.set_trace()

    def info(self, message):
        """
        Print an info message

        Example:: 

            - info: message to say

        .. note:: **Outputs:** message to say
        """
        self.printer.info(message)

    def step(self, message):
        """
        Print a step in the test plan

        Example::

            - step: Explanation of what this step does

        .. note:: **Outputs:** Explanation of what this step does
        """
        self.printer.step(message)

    def todo(self, message):
        """
        Print a todo note

        Example::

            - todo: This is a todo note

        .. note:: **Outputs:** This is a todo note
        """
        self.printer.todo(message)

    def wait(self, seconds):
        """
        Wait for a number of seconds 

        Example::

            - wait: 5

        .. note:: Waits for 5 seconds
        """
        time.sleep(seconds)

    def screenshot(self, options):
        """
        Take a screenshot and save it to `--screenshot-location`
        
        **Parameters**

        +------------+----------+-------------------------------------------+-----------------------------------------------------+
        | Name       | Required | Default                                   | Description                                         |
        +------------+----------+-------------------------------------------+-----------------------------------------------------+
        | image_name | no       | The title of the current page (slugified) | The name to save this screenshot as                 |
        +------------+----------+-------------------------------------------+-----------------------------------------------------+
        | widths     | no       | Current window size                       | A list of image sizes to use for screenshots.       |
        +------------+----------+-------------------------------------------+-----------------------------------------------------+
        

        **Examples:**

        .. code-block:: yaml

            # simplest:
            screenshot: {}

            # specify a custom name: 
            screenshot:
              - image_name: cool-screenshot

            # specify a list of sizes:
            screenshot:
              - image_name: cool-screenshot
              - widths: 
                  - 360
                  - 640
                  - 1024

        .. note:: **TODO:** width should be an array
        """
        widths = options.get('widths', None)
        image_name = options.get('image_name', None)

        if image_name is None:
            image_name = self.b.url.replace("https://","").replace("http://","").replace("/","-")
        
        base_name = '{}/{}' . format(self.screenshot_location, image_name)

        if widths is not None:
            for width in widths:
                self.b.driver.set_window_size(width, 1000)
                save_as = '{}-{}.png' . format(base_name, width)
                self.b.driver.save_screenshot(save_as)
        else:
            save_as = '{}.png' . format(base_name)
            self.b.driver.save_screenshot(save_as)
 
    def resize_window(self,options):
        """        
        Resize the current window. Useful for testing responsive layouts

        **Parameters**

        +--------+----------+---------+----------------------+
        | Name   | Required | Default | Description          |
        +--------+----------+---------+----------------------+
        | width  | no       | 1024    | The width in pixels  |
        +--------+----------+---------+----------------------+
        | height | no       | 1000    | The height in pixels |
        +--------+----------+---------+----------------------+
        
        **Examples:**

        .. code-block:: yaml

            # no arguments (1024x1000)
            resize_window: {}

            # specify width and height
            resize_window:
              width: 640
              height: 800

        """
        width = options.get('width', 1024)
        height = options.get('width', 1000)

        self.b.driver.resize(width, height)




    def click(self, selector):
        button_exists = self.expect_element(selector, selector)
        button = self.b.find_by_css(selector)
        if button_exists:
            self.printer.step("Click button: {0}" . format (button.first.text) )
            button.first.click()
        else:
            self.printer.todo("Missing button: {0}" . format(selector) )

    def click_first_visible(self, selector):

        all_items = self.b.find_by_css(selector)
        visible_items = self._get_visible(all_items)

        if len(visible_items) > 0:
            button = visible_items[0]        
            self.printer.step("Click button: {0}" . format (button.text) )
            button.click()
        else:
            message = "No visible buttons matching: {0}" . format(selector)
            self.expectation.assert_true(False, message )
                
    def select(self, selector_and_value):

        selector, value = selector_and_value.items()[0]
        el_exists = self.expect_element(selector, selector)
        if el_exists:      
            self.b.find_by_css(selector).first.select(value)
        else: 
            self.printer.todo("Missing select: {0}" . format(selector) )

    def select_random(self, selector):
        '''
        Will select a random value from the first visible 
        element matching the provided selector
        '''
        
        items = self.b.find_by_css(selector)
        visible_items = self._get_visible(items)

        if len(visible_items) > 0:
            select = visible_items[0]
            options = select.find_by_css("option")
            random_option = random.choice(options)
            random_option._element.click()
            self.printer.step("Select: {0}" . format (random_option.text) )
        else:
            message = "No visible select dropdowns matching: {0}" . format(selector)
            self.expectation.assert_true(False, message )

    def check(self, selector):  
        
        el_exists = self.expect_element(selector, selector)

        if el_exists:        
            self.b.find_by_css(selector).first.check()
        else: 
            self.printer.todo("Missing radio/checkbox: {0}" . format(selector) )

    def uncheck(self, selector):
        
        el_exists = self.expect_element(selector, selector)

        if el_exists:        
            self.b.find_by_css(selector).first.uncheck(value)
        else: 
            self.printer.todo("Missing radio/checkbox: {0}" . format(selector) )

    def wait_for_element(self, selector):
        element_is_available = self.b.is_element_present_by_css(selector, wait_time=self.wait_time)
        self.printer.step("waiting for {0} to load" .format (selector) )
        self.expectation.assert_true(element_is_available, "Element has loaded: {0}" . format (selector) )
        

    def wait_for_text(self, str):
        text_is_available = self.b.is_text_present(str, wait_time=DEFAULT_WAIT_TIME)
        self.printer.step("waiting for text: {0}" .format (str) )
        try:
            self.expectation.assert_true(text_is_available, "text {0} has loaded" .format (str) )
        except:
            pass
        

    def _get_visible(self, items):
        return [item for item in items if item.visible]
    
