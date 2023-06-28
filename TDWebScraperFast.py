from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import os
import time

# initialize the driver
options = Options()

#************************#
#IMPORTANT AND ONLY STEP WITHIN CODE:
#CHANGE THIS FILE PATH TO APPROPRIATE DIRECTORY, DO SO WITHIN QUOTATIONS, DO NOT REMOVE THE r BEFORE QUOTES
save_dir = r"C:\NxID\Dad\Statements"
#************************#

# Set Firefox's preferences for downloads
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
driver.get("https://etreasury.td.com/rwd-web/main/accounts/statements")  

input("Please log in manually, wait for the landing page to load then press Enter to continue...")
startPoint = int(input("If the app has crashed at a certain option(the most recent should be listed in the console prior to the option name in the previously running command prompt); please type the most recent option number-2(otherwise begin from the start by typing 0 and pressing Enter).\n"))
'''
def wait_for_spinner_to_disappear(driver, timeout, poll_frequency):
    end_time = time.time() + timeout
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, 'div.spinner.loading')
            time.sleep(poll_frequency)  # Pause a moment before trying again
            if time.time() > end_time:
                raise TimeoutException("Spinner did not disappear after waiting for {} seconds.".format(timeout))
        except NoSuchElementException:
            break
'''
# loop over all the options
i=startPoint
while True:
    path_to_watch = save_dir
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    if(i == startPoint):
        time.sleep(1)
        # click the "Accounts" dropdown
        accounts_dropdown = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'navigation_accounts')))
        accounts_dropdown.click()

        # click the "Statements" button
        statements_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'navigation_accounts_statements')))
        statements_button.click()

        # find the dropdown menu
        dropdown = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'stmtAccountcombobox')))
        dropdown.click()  # click to open the dropdown

        #grabs the length of all options to know when to terminate program
        options = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, '//ol-option[contains(@class, "ol-option option")]')))
        num_options = len(options)
        print(f'The dropdown has {num_options} options.')

        #closes dropdown after counting elements
        ActionChains(driver).move_to_element(dropdown).click().perform()
        time.sleep(1)
        i += 1

    if i % 100 == 0 and i > 0: #this if statement clears memory being used by Firefox by refreshing the page and resuming where it left off
        driver.execute_script('window.localStorage.clear();')
        driver.execute_script('window.sessionStorage.clear();')
        driver.refresh() 
        
        time.sleep(65)
        
        # click the "Accounts" dropdown
        accounts_dropdown = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'navigation_accounts')))
        accounts_dropdown.click()

        # click the "Statements" button
        statements_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'navigation_accounts_statements')))
        statements_button.click()

        # find the dropdown menu
        dropdown = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'stmtAccountcombobox')))
        dropdown.click()  # click to open the dropdown
        time.sleep(5)

        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//ol-option[contains(@class, "ol-option option")]')))
        
        option = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'ol-option.ol-option.option:nth-child({i + 1})')))
        driver.execute_script("arguments[0].scrollIntoView();", option)
        print(f"Option {i}: {option.text}")

        option_text = option.text 
        parts = option_text.split(" - ")  # Split the string into parts
        if len(parts) >= 2:  # Make sure we have at least two parts
            account_number = parts[-2]  # The account number is the second to last part
        
        ActionChains(driver).move_to_element(option).click().perform()         

        try: 
            statement_dropdown = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span#statementType_displayText')))
            ActionChains(driver).move_to_element(statement_dropdown).click().perform()
            time.sleep(0.8)
            statement_option = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ol-option#statementType_option_CBKAcctStmt')))
            ActionChains(driver).move_to_element(statement_option).click().perform()
        except TimeoutException:
            statement_dropdown = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span#statementType_displayText')))
            ActionChains(driver).move_to_element(statement_dropdown).click().perform()
            time.sleep(0.8)
            statement_option = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ol-option#statementType_option_CBKAcctStmt')))
            ActionChains(driver).move_to_element(statement_option).click().perform()
    else:   
        # click the dropdown again as it closes after each selection
        dropdown = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'stmtAccountcombobox')))
        ActionChains(driver).move_to_element(dropdown).click().perform()
        try: 
            option = driver.find_element(By.CSS_SELECTOR, f'ol-option.ol-option.option:nth-child({i + 1})')
        except NoSuchElementException:
            print(f"Option {i} is already saved or does not exist")
            close_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'close_dialog')))
            close_button.click()
            i += 1
            continue
        driver.execute_script("arguments[0].scrollIntoView();", option)
        time.sleep(1.5)
        print(f"Option {i}: {option.text}")
        
        option_text = option.text 
        parts = option_text.split(" - ")  # Split the string into parts
        if len(parts) >= 2:  # Make sure we have at least two parts
            account_number = parts[-2]  # The account number is the second to last part

        # click the option
        ActionChains(driver).move_to_element(option).click().perform()

    try:
        if(i == startPoint+1):
        # select the "Account Statements" option from the second dropdown
            try: 
                statement_dropdown = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span#statementType_displayText')))
                ActionChains(driver).move_to_element(statement_dropdown).click().perform()
                time.sleep(0.8)
                statement_option = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ol-option#statementType_option_CBKAcctStmt')))
                ActionChains(driver).move_to_element(statement_option).click().perform()
            except TimeoutException:
                statement_dropdown = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span#statementType_displayText')))
                ActionChains(driver).move_to_element(statement_dropdown).click().perform()
                time.sleep(0.8)
                statement_option = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ol-option#statementType_option_CBKAcctStmt')))
                ActionChains(driver).move_to_element(statement_option).click().perform()

        WebDriverWait(driver, 50).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'span#statementType_displayText'), 'Account Statements'))
        
        # click the "View Statement" button
        button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'btnViewStatement')))
        button.click()

        time.sleep(2.8)
        
        try:
            view_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'btnViewundefined')))
        except NoSuchElementException:
            print(f"No view button for option {i}")
            close_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'close_dialog')))
            close_button.click()
            i += 1
            continue
        except TimeoutException:
            print(f"Timeout while waiting for view button for option {i}")
            close_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'close_dialog')))
            close_button.click()
            i += 1
            continue

        view_button.click()

        time.sleep(8)
        #SAVE THE PDF
        
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        if added:
            new_file = os.path.join(path_to_watch, added[0])
            # get option text
            option_text = account_number + "_" + "20230531_" + str(i)
            new_filename = os.path.join(path_to_watch, option_text + ".pdf")
            os.rename(new_file, new_filename)
            print("Saved account file:", option_text + ".pdf")


        # switch back to the original window
        # go back to the original page (or however you want to navigate)
        close_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'close_dialog')))
        close_button.click()
        
        i += 1
    except Exception as e:
        print(f"An unexpected exception of type {type(e).__name__} occurred.")
        i += 1
        print(e.args)
    if(i == num_options-1):
        break;

#close the driver
print("Program finished downloading all statements. Program will now exit.")
driver.close()
driver.quit()
