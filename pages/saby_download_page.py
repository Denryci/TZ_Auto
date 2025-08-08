from pages.base_page import BasePage
from selenium import webdriver

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
            self.driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": download_dir
            })

    # Скачать файл по клику по ссылке
    def file_download(self):
        self.driver.find_element(*self.DOWNLOAD_BUTTON).click()