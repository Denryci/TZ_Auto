from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:

    # Локаторы основных ссылок между страницами
    CONTACTS_LINK_LOCATOR = ("xpath", "//a[@href='/contacts']")
    TENSOR_LINK_LOCATOR = ("xpath", "//a[@href='https://tensor.ru/' and @class='sbisru-Contacts__logo-tensor mb-12']")
    TENSOR_ABOUT_LINK_LOCATOR = ('xpath', "//a[@href='/about']")
    DOWNLOADS_LINK_LOCATOR = ('xpath', "//a[@href='/download'] ")

    # Инициализация конструктора (и передача драйвера)
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Открытие страницы по ссылке
    def open(self):
        self.driver.get(self.PAGE_URL)

    # Получить ссылку на текущую страницу
    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title