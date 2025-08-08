import pytest
from selenium.common.exceptions import NoSuchElementException

from pages.saby_page import SabyPage
from pages.tensor_about_page import TensorAboutPage

class TestTensorBlockAndPhotos:
    def test_check_tensor_block_StrengthAndPeople(self):

        # 1. Перейдём на главную страницу
        saby_page = SabyPage(self.driver)
        saby_page.open()

        # 2. Перейдём Saby -> Saby/contacts
        contact_page = saby_page.go_to_contacts()

        # 3. Перейдём Saby/contacts -> Tensor
        tensor_page = contact_page.go_to_tensor()

        # 4. Проверим блок "Сила в людях". В случае ненахождения find_element возвращает AssertError
        try:
            strength_block = tensor_page.driver.find_element(*tensor_page.US_DIV)
        except NoSuchElementException:
            assert False, "Элемент US_DIV не найден на странице"

        assert "Сила в людях" in strength_block.text, "В блоке 'Сила в людях' ошибка с текстом"

        # 5. Переходим в раздел "Подробнее", Tensor -> Tensor/about
        about_page = tensor_page.go_to_tensor_about()

        # 6. Проверим, что ссылка правильная
        assert about_page.get_current_url() == TensorAboutPage.PAGE_URL, "Это не страница 'О Тензоре'"

        # 7. Проверим, что фотографии в разделе "Работаем" имеют одинаковую ширину и высоту соответственно
        photos = about_page.get_work_photos()
        if len(photos) > 1:
            first_width = photos[0]['width']
            first_height = photos[0]['height']

            assert all(photo['width'] == first_width for photo in photos), 'Ширина фотографий отличается'
            assert all(photo['height'] == first_height for photo in photos), 'Высота фотографий отличается'
