from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException, StaleElementReferenceException
import os
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as parse_date

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
#last_day_of_last_month = (now.replace(day=1) - relativedelta(days=1)).day
first_day_this_month = now.replace(day=1)
#first_day_last_month = first_day_this_month - relativedelta(months=1)

last_day_of_last_month = first_day_this_month - relativedelta(days=1)
first_day_last_month = first_day_this_month - relativedelta(months=1)

date_str = f"{last_month.month:02d}{last_day_of_last_month.day:02d}{last_month.year}"

first_date_str = f"{last_month.month:02d}/{first_day_last_month.day:02d}/{last_month.year}"
last_date_str = f"{last_month.month:02d}/{last_day_of_last_month:02d}/{last_month.year}"

dir_name = f"CitiStatements{date_str}"
save_dir = os.path.join(os.getcwd(), dir_name)

if not os.path.exists(save_dir):
    # Create the directory
    os.makedirs(save_dir)

options = Options()

options.set_preference("browser.download.folderList", 2)  # 0 means to download to the desktop, 1 means to download to the default "Downloads" directory, 2 means to use the directory you specify in "browser.download.dir"
options.set_preference("browser.download.dir", save_dir)  # path to directory where to save downloads
options.set_preference("browser.download.useDownloadDir", True)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # MIME type of pdf files
options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")  # to disable the pdf viewer and download pdf files
options.set_preference("pdfjs.disabled", True)  # to disable the built-in PDF viewer
options.set_preference("browser.cache.disk.enable", False)
options.set_preference("browser.cache.memory.enable", False)
options.set_preference("browser.cache.offline.enable", False)
options.set_preference("network.http.use-cache", False)
options.set_preference("browser.sessionhistory.max_total_viewers", 0)

driver = webdriver.Firefox(options=options)

driver.maximize_window()

# replace with your actual URL
driver.get("https://businessaccess.citibank.citigroup.com/cbusol/ang/#/login")  

input("Please log in manually, wait for the landing page to load then press Enter to continue...")
startPoint = load_i_from_file(save_dir)
# loop over all the options
i=startPoint
while True:
    if (i == startPoint):
        information = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Information Reporting')))
        information.click()

        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'classicFrame')))
        time.sleep(5)
        driver.switch_to.frame("BAmainFrmId")

        bank_statements_link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Bank Statements')))
        bank_statements_link.click()

        try:
            # Wait for the alert to appear
            WebDriverWait(driver, 20).until(EC.alert_is_present())

            # Switch to the alert
            alert = driver.switch_to.alert

            # Accept the alert
            alert.accept()
        except NoAlertPresentException:
            # No alert was present, do nothing
            pass

    driver.switch_to.default_content() 

    try:
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'classicFrame')))
        time.sleep(2)
        driver.switch_to.frame("BAmainFrmId")
    except TimeoutException:
        print("Could not switch to the frame 'classicFrame'.")
        time.sleep(3)
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'classicFrame')))
        driver.switch_to.frame("BAmainFrmId")

    dropdown = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'groupName')))
        
    # Create a Select object
    select = Select(dropdown)
        
    # Select option by visible text
    select.select_by_visible_text('NOT GROUPED')

    account_dropdown = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'selectedAccount')))
    select_option = Select(account_dropdown)

    # Select option by value
    select_option.select_by_index(i)

    continue_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'continue')))
    continue_button.click()

    links = driver.find_elements(By.TAG_NAME, 'a')

    # Iterate over all links
    for link in links:
        # Try to parse the link text as a date
        try:
            link_date = parse_date(link.text.strip())
            #print(link_date)
        except ValueError:
            # Skip this link if its text cannot be parsed as a date
            continue

        # Check if the link date falls within the last month
        if first_day_last_month <= link_date <= last_day_of_last_month:
            # Click the link
            link.click()
            break
    
    driver.back()
    save_i_to_file(i, save_dir)
    i += 1

