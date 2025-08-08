from pages.base_page import BasePage
from pages.tensor_page import TensorPage
from selenium.common.exceptions import NoSuchElementException

class SabyContactsPage(BasePage):

    # Локаторы на основные элементы страницы
    PAGE_URL = "https://saby.ru/contacts"
    CHANGE_REGION = ("xpath", "//div[@class='sbis_ru-container sbisru-Contacts__relative']//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    PARTNERS_LIST = ("xpath", "(//div[@data-qa='items-container'])[1]")
    KAMCHATKA_KRAY = ("xpath", "//span[@title='Камчатский край']")
    YAROSLAVL_OBLAST = ("xpath", "//span[@title='Ярославская обл.']")
    CLOSE_MENU_BTN = ("xpath", "//div[@class='sbis_ru-Region-Panel__header-close ws-flex-shrink-0']")

    KAMCHATKA_KRAY_CODE = "41-kamchatskij-kraj"
    YAROSLAVL_OBLAST_CODE = "76-yaroslavskaya-oblast"

    # Переход по ссылке Saby/contacts -> Tensor (target=_blank)
    def go_to_tensor(self):
        original_window = self.driver.current_window_handle

        self.driver.find_element(*self.TENSOR_LINK_LOCATOR).click()

        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

        return TensorPage(self.driver)

    def extract_url_region(self):
        url = self.get_current_url()
        url_parts = url.split('/')
        end = url_parts[-1]
        end_parts = end.split('?')
        return end_parts[0]

    def extract_title_region(self):
        title = self.get_title()
        title_parts = title.split(' — ')
        return title_parts[-1]

    def get_partners(self):
        try:
            partner_list = self.driver.find_element(*self.PARTNERS_LIST)
            partners = partner_list.find_elements("css selector", "div div[data-qa='item']")
            partner_arr = []
            for partner in partners:
                item_key = partner.get_attribute("item-key")
                if item_key:
                    partner_arr.append(item_key)
            return partner_arr
        except NoSuchElementException:
            assert False, "Список регионов не обнаружен на странице"
