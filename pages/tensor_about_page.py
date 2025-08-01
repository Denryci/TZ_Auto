from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class TensorAboutPage(BasePage):

    PAGE_URL = "https://tensor.ru/about"
    WORK_GALLERY = ("xpath", "//div[@class='tensor_ru-container tensor_ru-section tensor_ru-About__block3']//div[@class='s-Grid-container']")

    def return_about_photos_sizes(self):
        gallery = self.wait.until(EC.presence_of_element_located(self.WORK_GALLERY))
        images = gallery.find_elements(By.TAG_NAME, "img")

        if not images:
            return []

        sizes = []
        for img in images:
            self.wait.until(EC.visibility_of(img))

            size = {
                'width': img.size['width'],
                'height': img.size['height'],
            }

            sizes.append(size)
        return sizes
