import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.saby_page import SabyPage
from pages.tensor_about_page import TensorAboutPage

class TestTensorBlockAndPhotos:
    def test_check_tensor_block_StrengthAndPeople(self):
        # Настройка логгера
        logger = logging.getLogger('tensor_test')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.info("Начало теста: проверка блока 'Сила в людях' и фотографий")

        try:
            # 1. Перейдём на главную страницу
            logger.info("Шаг 1: Открытие главной страницы Saby")
            saby_page = SabyPage(self.driver)
            saby_page.open()

            # 2. Перейдём Saby -> Saby/contacts
            logger.info("Шаг 2: Переход на страницу контактов")
            contact_page = saby_page.go_to_contacts()

            # 3. Перейдём Saby/contacts -> Tensor
            logger.info("Шаг 3: Переход на страницу Tensor")
            tensor_page = contact_page.go_to_tensor()

            # 4. Проверим блок "Сила в людях".
            logger.info("Шаг 4: Проверка блока 'Сила в людях'")
            strength_block = WebDriverWait(tensor_page.driver, 10).until(
                EC.visibility_of_element_located(tensor_page.US_DIV)
            )

            # Проверяем что текст в блоке соответствует "Сила в людях"
            logger.info(f"Проверка текста в блоке. Ожидаемый текст: {tensor_page.US_TEXT}")
            assert tensor_page.US_TEXT in strength_block.text, "В блоке 'Сила в людях' ошибка с текстом"
            logger.info("Текст в блоке соответствует ожидаемому")

            # 5. Переходим в раздел "Подробнее", Tensor -> Tensor/about
            logger.info("Шаг 5: Переход на страницу 'О Тензоре'")
            about_page = tensor_page.go_to_tensor_about()

            # 6. Проверим, что ссылка правильная
            current_url = about_page.get_current_url()
            logger.info(f"Проверка URL. Текущий URL: {current_url}, ожидаемый: {TensorAboutPage.PAGE_URL}")
            assert current_url == TensorAboutPage.PAGE_URL, "Это не страница 'О Тензоре'"
            logger.info("URL страницы соответствует ожидаемому")

            # 7. Проверим, что фотографии в разделе "Работаем" имеют одинаковую ширину и высоту соответственно
            logger.info("Шаг 7: Проверка фотографий в разделе 'Работаем'")
            photos = about_page.get_work_photos()

            if len(photos) > 1:
                first_width = photos[0]['width']
                first_height = photos[0]['height']
                logger.info(f"Первая фотография: ширина={first_width}, высота={first_height}")

                # Логируем размеры всех фотографий
                for i, photo in enumerate(photos, 1):
                    logger.debug(f"Фото {i}: ширина={photo['width']}, высота={photo['height']}")

                assert all(photo['width'] != 0 for photo in photos), 'Ширина фотографий нулевая'
                assert all(photo['height'] != 0 for photo in photos), 'Высота фотографий нулевая'
                logger.info("Все фотографии имеют ненулевые размеры")

                assert all(photo['width'] == first_width for photo in photos), 'Ширина фотографий отличается'
                assert all(photo['height'] == first_height for photo in photos), 'Высота фотографий отличается'
                logger.info("Все фотографии имеют одинаковые размеры")

            elif len(photos) == 0:
                logger.error("Фотографии отсутствуют")
                assert False, "Фотографии отсутствуют"
            else:
                logger.warning("Найдена только одна фотография - сравнение невозможно")

            logger.info("Тест успешно завершен")

        except AssertionError as ae:
            logger.error(f"Ошибка проверки: {str(ae)}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка во время выполнения теста: {str(e)}")
            raise