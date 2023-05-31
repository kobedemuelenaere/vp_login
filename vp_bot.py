from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException,NoSuchElementException, TimeoutException
import time

username = "luka.demuelenaere@hotmail.com"
password = "?Lukie2842$"
    
def automate_login(driver, username, password, website=None):
    
    if website is None:
        website = "https://vp.lpl-cloud.com/en/login"

    # Open the website
    while True:
        driver.get(website)
        try:
            WebDriverWait(driver, 0.3).until(EC.presence_of_element_located((By.XPATH, '//div[@class="vp-page-info"]/h2[contains(text(), "A new product selection is being prepared")]')))
        except TimeoutException:
            break
        
    

    # Wait for the "ACCEPT NECESSARY COOKIES" button to be present and click it
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler"))).click()

    # Wait for the username field to be present, clear it, and enter the username
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "j_username"))).send_keys(username)

    # Wait for the password field to be present, clear it, and enter the password
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "j_password"))).send_keys(password)

     
    # Wait for the "Login" button to be present and click it
    while True:
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//button[normalize-space(text())="Login"]'))).click()
            break
        except ElementClickInterceptedException:
            continue

def check_items_in_dom(driver, path):
    print(path)
    for title in path:
        if title == '':
            return True
        try:
            WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH, f'//a[@title="{title}"]')))
        except TimeoutException:
            print(f"check items: {title} not available")
            return False
    return True

def navigate_vp(driver, path):
    for title in path:
        # Wait for the "title" link to be present and click it
        while True:
            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, f'//a[@title="{title}"]'))).click()
                break
            except ElementClickInterceptedException:
                continue

def access_site_loop(path = [], website = "", restart_driver=False):
    # Setup Firefox options
    options = Options()
    #options.add_argument('-headless')

    # Set the location of the geckodriver executable
    driver = webdriver.Firefox(options=options)
    
    while True:
        # Login
        
        automate_login(driver,username, password)

        # Check items and navigate if they are present
        if check_items_in_dom(driver,path):
            if website == "":
                navigate_vp(driver,path)
            else:
                driver.get(website)
            break
        else:
            # Clear cookies
            driver.delete_all_cookies()
            if restart_driver:
                driver.quit()
                driver = webdriver.Firefox(options=options)
    

if __name__ == "__main__":
    
    # Setup Firefox options
    options = Options()
    #options.add_argument('-headless')

    # Set the location of the geckodriver executable
    driver = webdriver.Firefox(options=options)
    automate_login(driver,username, password)

    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "vp-ico-cart-full") or contains(@class, "vp-ico-cart")]'))).click()


    while True:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//a[normalize-space(text())="Add to bag"]'))).click()

