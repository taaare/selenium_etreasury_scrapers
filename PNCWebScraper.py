from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import os
import re
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

def save_i_to_file(i, save_dir):
    # Use 'w' mode to overwrite the file content with the new value of 'i'
    with open(os.path.join(save_dir, "i.txt"), 'w') as file:
        file.write(str(i))

def load_i_from_file(save_dir):
    file_path = os.path.join(save_dir, "i.txt")
    # Check if the file exists
    if os.path.exists(file_path):
        # Use 'r' mode to read the file content
        with open(file_path, 'r') as file:
            content = file.read()
            return int(content)
    return 1  # If the file does not exist, return 0

now = datetime.now()
last_month = now - relativedelta(months=1)
last_day_of_last_month = (now.replace(day=1) - relativedelta(days=1)).day
first_day_this_month = now.replace(day=1)
first_day_last_month = first_day_this_month - relativedelta(months=1)

date_str = f"{last_month.month:02d}{last_day_of_last_month:02d}{last_month.year}"

first_date_str = f"{last_month.month:02d}/{first_day_last_month.day:02d}/{last_month.year}"
last_date_str = f"{last_month.month:02d}/{last_day_of_last_month:02d}/{last_month.year}"

# initialize the driver
options = Options()

dir_name = f"PNCStatements{date_str}"
save_dir = os.path.join(os.getcwd(), dir_name)

if not os.path.exists(save_dir):
    # Create the directory
    os.makedirs(save_dir)

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

startPoint = load_i_from_file(save_dir)

index = startPoint # because index 0 is the default option "Select an account"
while True:
    path_to_watch = save_dir
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    try:
        # Re-acquire the frame and dropdown element references
        driver.switch_to.default_content() # first switch back to the main document
        frame = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'contentIframe')))
        driver.switch_to.frame(frame) # switch to the frame
        dropdown = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'account'))) # find the dropdown
        
        # select option by index using JavaScript
        driver.execute_script("arguments[0].selectedIndex = {}; arguments[0].dispatchEvent(new Event('change'));".format(index), dropdown)
        
        time.sleep(5) # give it some time to load the new page, adjust as needed

        print_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Print Statement')))
        print_button.click()

        time.sleep(2)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        if added:
            new_file = os.path.join(path_to_watch, added[0])
            account_number = re.search(r'_([0-9]+)_', added[0]).group(1)
            # get option text
            option_text = account_number + "_" + date_str + "_" + str(index)
            new_filename = os.path.join(path_to_watch, option_text + ".pdf")
            os.rename(new_file, new_filename)
            print("Saved account file:", option_text + ".pdf")
        save_i_to_file(index, save_dir)
        index += 1
    except Exception as e: # when there are no more options, we'll get an exception
        print("End of options reached or the page has been refreshed. Loop ended at index: ", index)
        print("Exception: ", e)
        break

