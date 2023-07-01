from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import os
import time

# initialize the driver
options = Options()

save_dir = r"C:\NxID\Dad\Statements"

# Set Firefox's preferences for downloads
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", save_dir)
options.set_preference("browser.download.useDownloadDir", True)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
options.set_preference("pdfjs.disabled", True)
options.set_preference("browser.cache.disk.enable", False)
options.set_preference("browser.cache.memory.enable", False)
options.set_preference("browser.cache.offline.enable", False)
options.set_preference("network.http.use-cache", False)
options.set_preference("browser.sessionhistory.max_total_viewers", 0)

driver = webdriver.Firefox(options=options)

driver.maximize_window()

# replace with your actual URL for PNC's Pinacle Treasury
driver.get("https://www.treasury.pncbank.com/idp/esec/login.ht")  

input("Please log in manually, wait for the landing page to load then press Enter to continue...")

#close_button = driver.find_element(By.ID, 'splash-91626-close-button')
#driver.execute_script("arguments[0].click();", close_button)

dda_element = driver.find_element(By.ID, 'DDAST')
driver.execute_script("arguments[0].click();", dda_element)

time.sleep(10)

# locate the select element
frame = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'contentIframe')))
driver.switch_to.frame(frame)

dropdown = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'account')))
dropdown.click()

index = 1 # because index 0 is the default option "Select an account"
while True:
    try:
        # Re-acquire the frame and dropdown element references
        driver.switch_to.default_content() # first switch back to the main document
        frame = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'contentIframe')))
        driver.switch_to.frame(frame) # switch to the frame
        dropdown = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'account'))) # find the dropdown
        
        # select option by index using JavaScript
        driver.execute_script("arguments[0].selectedIndex = {}; arguments[0].dispatchEvent(new Event('change'));".format(index), dropdown)
        
        time.sleep(5) # give it some time to load the new page, adjust as needed

        print_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Print Statement')))
        print_button.click()

        index += 1
    except Exception as e: # when there are no more options, we'll get an exception
        print("End of options reached or the page has been refreshed. Loop ended at index: ", index)
        print("Exception: ", e)
        break

