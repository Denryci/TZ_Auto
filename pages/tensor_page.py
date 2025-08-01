from pages.base_page import BasePage
from pages.tensor_about_page import TensorAboutPage

class TensorPage(BasePage):

    PAGE_URL = "https://tensor.ru/"
    US_DIV = ("xpath", "//div[@class='tensor_ru-Index__block4-content tensor_ru-Index__card']")

    def go_to_tensor_about(self):
        self.driver.find_element(*self.TENSOR_ABOUT_LINK_LOCATOR).click()
        return TensorAboutPage(self.driver)