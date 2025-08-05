from pages.base_page import BasePage
from pages.saby_contacts_page import SabyContactsPage
from pages.saby_download_page import SabyDownloadPage

class SabyPage(BasePage):

    # Локаторы основных элементов на странице
    PAGE_URL = "https://saby.ru/"

    # Переход по ссылке Saby -> Saby/contacts
    def go_to_contacts(self):
        self.driver.find_element(*self.CONTACTS_LINK_LOCATOR).click()
        return SabyContactsPage(self.driver)

    # Переход по ссылке Saby -> Saby/download
    def go_to_download(self):
        self.driver.find_element(*self.DOWNLOADS_LINK_LOCATOR).click()
        return SabyDownloadPage(self.driver)

