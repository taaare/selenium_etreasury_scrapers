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

dda_element = driver.find_element(By.ID, 'DDAST')
driver.execute_script("arguments[0].click();", dda_element)

time.sleep(10)

# locate the select element
dropdown = driver.execute_script("return document.getElementsByName('account')[0];")
driver.execute_script("arguments[0].click();", dropdown)

index = 1
while True:
    try:
        # select option by index using JavaScript
        driver.execute_script("arguments[0].selectedIndex = {}; arguments[0].dispatchEvent(new Event('change'));".format(index), dropdown)

        time.sleep(1)
        index += 1
    except StaleElementReferenceException:
        print("End of options reached or the page has been refreshed. Loop ended at index: ", index)
        break