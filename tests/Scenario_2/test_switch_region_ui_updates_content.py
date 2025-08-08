import logging
from pages.saby_page import SabyPage
from pages.saby_contacts_page import SabyContactsPage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSwitchRegion:
    def test_switch_region_ui_updates_content(self):
        # Настройка логгера
        logger = logging.getLogger('region_switch_test')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.info("Начало теста: проверка переключения региона и обновления контента")

        try:
            # 1. Переходим на главную страницу
            logger.info("Шаг 1: Открытие главной страницы Saby")
            saby_page = SabyPage(self.driver)
            saby_page.open()

            # 2. Переходим Saby -> Контакты
            logger.info("Шаг 2: Переход на страницу контактов")
            contacts_page = saby_page.go_to_contacts()

            # 3. Проверить, что в блоке наш регион (и в url, и в title) и есть список партнеров
            logger.info("Шаг 3: Проверка региона по умолчанию (Ярославская область)")
            title = contacts_page.extract_title_region()
            url_code = contacts_page.extract_url_region()
            yar_partners_list = contacts_page.get_partners()

            logger.info(
                f"Проверка заголовка региона. Ожидаемый: {contacts_page.YAROSLAVL_OBLAST_TEXT}, текущий: {title}")
            assert title == contacts_page.YAROSLAVL_OBLAST_TEXT, "Регион страницы не соответствует значению в блоке CHANGE_REGION"

            logger.info(
                f"Проверка кода региона в URL. Ожидаемый: {contacts_page.YAROSLAVL_OBLAST_CODE}, текущий: {url_code}")
            assert url_code == contacts_page.YAROSLAVL_OBLAST_CODE, "Код региона в url не соответствует значению в блоке CHANGE_REGION"

            logger.info(f"Проверка списка партнеров. Найдено партнеров: {len([partner for partner in yar_partners_list if partner > 0])}")
            assert len(yar_partners_list) > 0, "Список партнёров Ярославской области пуст"
            assert any(partner > 0 for partner in yar_partners_list), "Партнёры отсутствуют в списке Ярославской области"

            try:
                logger.info("Проверка текста в элементе CHANGE_REGION")
                change_reg = contacts_page.driver.find_element(*contacts_page.CHANGE_REGION)
                assert change_reg.text == contacts_page.YAROSLAVL_OBLAST_TEXT_SHORT, "Регион изначально не Ярославская область"
                logger.info("Текст в CHANGE_REGION соответствует ожидаемому")
            except NoSuchElementException:
                logger.error("Элемент 'CHANGE_REGION' не был найден на странице")
                assert False, "Элемент 'CHANGE_REGION' не был найден на странице"

            # 4. Изменить регион на Камчатский край через UI
            logger.info("Шаг 4: Переключение региона на Камчатский край")
            contacts_page.driver.find_element(*contacts_page.CHANGE_REGION).click()
            contacts_page = SabyContactsPage(contacts_page.driver)

            # Ожидаем появления меню и кнопок (и жмём на текст Камчатский край)
            logger.info("Ожидание появления меню выбора региона")
            WebDriverWait(contacts_page.driver, 10).until(
                EC.visibility_of_element_located(contacts_page.KAMCHATKA_KRAY)
            ).click()

            # Ждем обновления страницы (можно ждать изменения URL)
            logger.info("Ожидание обновления URL после смены региона")
            WebDriverWait(contacts_page.driver, 10).until(
                lambda driver: contacts_page.KAMCHATKA_KRAY_CODE in driver.current_url
            )

            # Инициализируем новую страницу после обновления
            contacts_page = SabyContactsPage(self.driver)
            contacts_page = SabyContactsPage(contacts_page.driver)

            # 5. Проверим, что подставился регион, список партнёров изменился, url и title содержат информацию региона
            logger.info("Шаг 5: Проверка данных после смены региона")
            kamch_partners_list = contacts_page.get_partners()
            title = contacts_page.extract_title_region()
            url_code = contacts_page.extract_url_region()

            logger.info(
                f"Проверка нового заголовка региона. Ожидаемый: {contacts_page.KAMCHATKA_KRAY_TEXT}, текущий: {title}")
            assert title == contacts_page.KAMCHATKA_KRAY_TEXT, "Регион страницы не соответствует значению в блоке CHANGE_REGION"

            logger.info(
                f"Проверка нового кода региона в URL. Ожидаемый: {contacts_page.KAMCHATKA_KRAY_CODE}, текущий: {url_code}")
            assert url_code == contacts_page.KAMCHATKA_KRAY_CODE, "Код региона в url не соответствует значению в блоке CHANGE_REGION"

            logger.info(
                f"Проверка текста в CHANGE_REGION. Ожидаемый: {contacts_page.KAMCHATKA_KRAY_TEXT}, текущий: {change_reg.text}")
            assert change_reg.text == contacts_page.KAMCHATKA_KRAY_TEXT, "Значение CHANGE_REGION не изменилось на 'Камчатский край'"

            logger.info(f"Проверка нового списка партнеров. Найдено партнеров: {len([partner for partner in kamch_partners_list if partner > 0])}")
            assert len(kamch_partners_list) > 0, "Список партнёров Камчатского края пуст"
            assert any(partner > 0 for partner in kamch_partners_list), "Партнёры отсутствуют в списке Камчатского края"

            logger.info("Проверка, что списки партнеров изменились")
            assert yar_partners_list != kamch_partners_list, "Список партнеров не изменился"

            logger.info("Тест успешно завершен")

        except AssertionError as ae:
            logger.error(f"Ошибка проверки: {str(ae)}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка во время выполнения теста: {str(e)}")
            raise