from pages.base_page import BasePage
from pages.tensor_page import TensorPage

class SabyContactsPage(BasePage):

    # Локаторы на основные элементы страницы
    PAGE_URL = "https://saby.ru/contacts"
    CHANGE_REGION = ("xpath", "//div[@class='sbis_ru-container sbisru-Contacts__relative']//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    PARTNERS_LIST = ("xpath", "(//div[@data-qa='items-container'])[1]")
    KAMCHATKA_KRAY = ("xpath", "//span[@title='Камчатский край']")

    # Переход по ссылке Saby/contacts -> Tensor (target=_blank)
    def go_to_tensor(self):
        original_window = self.driver.current_window_handle

        self.driver.find_element(*self.TENSOR_LINK_LOCATOR).click()

        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

        return TensorPage(self.driver)
