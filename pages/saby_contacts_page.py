from pages.base_page import BasePage
from pages.tensor_page import TensorPage

class SabyContactsPage(BasePage):

    PAGE_URL = "https://saby.ru/contacts"
    CHANGE_REGION = ("xpath", "//div[@class='sbis_ru-container sbisru-Contacts__relative']//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    PARTNERS_LIST = ("xpath", "//div[contains(@class, 'controls-BaseControl__itemsContainer_7607b175-86fe-438d-8df8-cb56bc057eb4')]")

    def go_to_tensor(self):
        self.driver.find_element(*self.TENSOR_LINK_LOCATOR).click()
        return TensorPage(self.driver)