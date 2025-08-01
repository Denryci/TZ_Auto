from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    CONTACTS_LINK_LOCATOR = ("xpath", "//a[@href='/contacts']")
    TENSOR_LINK_LOCATOR = ("xpath", "//a[@href='https://tensor.ru/']")
    TENSOR_ABOUT_LINK_LOCATOR = ('xpath', "//a[@href='/about']")
    DOWNLOADS_LINK_LOCATOR = ('xpath', "//a[@href='/download'] ")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.PAGE_URL)