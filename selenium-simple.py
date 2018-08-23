import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from sauceclient import SauceClient
 
# This is the only code you need to edit in your existing scripts.
# The command_executor tells the test to run on Sauce, while the desired_capabilities
# parameter tells us which browsers and OS to spin up.
username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']
build = os.environ["TRAVIS_BUILD_NUMBER"]
tags = [os.environ["TRAVIS_PYTHON_VERSION"], "CI"]
sauce_client = SauceClient(username, access_key)
desired_cap = {
    'platform': "Mac OS X 10.12",
    'browserName': "chrome",
    'version': "latest",
    'build': build,
    'tags': tags,
}
driver = webdriver.Remote(
   command_executor='http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(username, access_key),
   desired_capabilities=desired_cap)
 
# This is your test logic. You can add multiple tests here.
driver.get("http://the-internet.herokuapp.com/disappearing_elements")

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Gallery"))
    )
    sauce_client.jobs.update_job(driver.session_id, passed=True)
except:
    sauce_client.jobs.update_job(driver.session_id, passed=False)
finally:
    driver.quit()
    
# gallery_link = driver.find_element_by_link_text("Gallery")
# assert "Sauce" in driver.title
# sauce_client.jobs.update_job(driver.session_id, passed=True) 

# This is where you tell Sauce Labs to stop running tests on your behalf.
# It's important so that you aren't billed after your test finishes.
# driver.quit()