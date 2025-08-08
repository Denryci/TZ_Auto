from pages.base_page import BasePage
from pages.tensor_about_page import TensorAboutPage

class TensorPage(BasePage):

    # Локаторы основных элементов на странице
    PAGE_URL = "https://tensor.ru/"
    US_DIV = ("xpath", "//div[@class='tensor_ru-Index__block4-content tensor_ru-Index__card']//p[@class='tensor_ru-Index__card-title tensor_ru-pb-16']")
    US_TEXT = "Сила в людях"

    # Переход по ссылке Tensor -> Tensor/about
    def go_to_tensor_about(self):
        self.driver.find_element(*self.TENSOR_ABOUT_LINK_LOCATOR).click()
        return TensorAboutPage(self.driver)