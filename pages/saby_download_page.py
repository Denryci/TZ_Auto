from pages.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SabyDownloadPage(BasePage):

    # Локаторы основных элементов страницы
    PAGE_URL = "https://saby.ru/download"
    DOWNLOAD_BUTTON = ("xpath", "//a[@href='https://update.saby.ru/SabyDesktop/master/win32/saby-setup.exe']")

    # Инициализация класса (для следующего скачивания установщика)
    def __init__(self, driver, download_dir=None):
        super().__init__(driver)
        if download_dir:
            self.set_download_directory(download_dir)

    # Настройка драйвера для скачивания установщика
    def set_download_directory(self, download_dir):
        if isinstance(self.driver, webdriver.Chrome):
            options = Options()
            options.add_argument("--safebrowsing-disable-download-protection")
            options.add_argument("safebrowsing-disable-extension-blacklist")
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_update": True,
                "safebrowsing_enabled": False
            }
            options.add_experimental_option("prefs", prefs)
            self.driver.capabilities.update(options.to_capabilities())

    # Скачать файл по ссылке
    def file_download(self):
        self.driver.find_element(*self.DOWNLOAD_BUTTON).click()