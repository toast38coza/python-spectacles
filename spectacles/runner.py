import click
from yamldriver import YAMLDriver
from splinter import Browser

# environment variables: 

@click.option('--out-location', default='./reports/specs', help='path to the directory where we will output the spec results')
@click.option('--spec-location', default='./specs', help='path to the directory containing your yml specs')
@click.option('--driver', default='phantomjs', help='Select the browser driver you would like to use (phantomjs, chrome, firefox)')
@click.argument('base-url')
@click.command()
def run(base_url, driver, spec_location, out_location):
    
    b = Browser(driver)
    yaml_driver = YAMLDriver(base_url, b)

    specs = "{}/*.yml" . format (spec_location)    
    yaml_driver.run_many(specs)
    b.quit()

if __name__ == '__main__':
    run()