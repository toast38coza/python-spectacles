import click
from yamldriver import YAMLDriver
from splinter import Browser

# environment variables: 

@click.option('--screenshot-location', default='./reports/screenshots', help='path where we will save screenshots')
@click.option('--out-location', default='./reports/specs', help='path to the directory where we will output the spec results')
@click.option('--spec-location', default='./specs/*.yml', help='A glob for finding spec files')
@click.option('--driver', default='firefox', help='Select the browser driver you would like to use (phantomjs, chrome, firefox)')
@click.argument('base-url')
@click.command()
def run(base_url, driver, spec_location, out_location, screenshot_location):
    
    b = Browser(driver)

    options = {
    	"out_location": out_location,
    	"screenshot_location": screenshot_location,
    }

    yaml_driver = YAMLDriver(base_url, b, options)
    yaml_driver.run_many(spec_location)
    b.quit()

if __name__ == '__main__':
    run()