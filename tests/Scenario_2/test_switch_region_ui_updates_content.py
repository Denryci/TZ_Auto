import pytest
from pages.saby_page import SabyPage
from pages.saby_contacts_page import SabyContactsPage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSwitchRegion:
    def test_switch_region_ui_updates_content(self):

        # 1. Переходим на главную страницу
        saby_page = SabyPage(self.driver)
        saby_page.open()

        # 2. Переходим Saby -> Контакты
        contacts_page = saby_page.go_to_contacts()

        # 3. Проверить, что в блоке наш регион (и в url, и в title) и есть список партнеров
        title = contacts_page.extract_title_region()
        url_code = contacts_page.extract_url_region()
        yar_partners_list = contacts_page.get_partners()

        assert title == "Ярославская область", "Регион страницы не соответствует значению в блоке CHANGE_REGION"
        assert url_code == contacts_page.YAROSLAVL_OBLAST_CODE, "Код региона в url не соответствует значению в блоке CHANGE_REGION"

        try:
            change_reg = contacts_page.driver.find_element(*contacts_page.CHANGE_REGION)
            assert change_reg.text == "Ярославская обл.", "Регион изначально не Ярославская область"
        except NoSuchElementException:
            assert False, "Элемент 'CHANGE_REGION' не был найден на странице"

        # 4. Изменить регион на Камчатский край через UI
        contacts_page.driver.find_element(*contacts_page.CHANGE_REGION).click()
        contacts_page = SabyContactsPage(contacts_page.driver)

        # Ожидаем появления меню и кнопок (включая Камчатский край)
        WebDriverWait(contacts_page.driver, 10).until(
            EC.visibility_of_element_located(contacts_page.KAMCHATKA_KRAY)
        ).click()

        # Ждем обновления страницы (можно ждать изменения URL или появления нового региона)
        WebDriverWait(contacts_page.driver, 10).until(
            lambda driver: contacts_page.KAMCHATKA_KRAY_CODE in driver.current_url
        )

        # Инициализируем новую страницу после обновления
        contacts_page = SabyContactsPage(self.driver)

        # Теперь можно создать новый экземпляр страницы
        contacts_page = SabyContactsPage(contacts_page.driver)

        # 5. Проверить, что подставился регион, список партнёров изменился, url и title содержат информацию региона
        kamch_partners_list = contacts_page.get_partners()
        title = contacts_page.extract_title_region()
        url_code = contacts_page.extract_url_region()
        assert title == "Камчатский край", "Регион страницы не соответствует значению в блоке CHANGE_REGION"
        assert url_code == contacts_page.KAMCHATKA_KRAY_CODE, "Код региона в url не соответствует значению в блоке CHANGE_REGION"
        assert change_reg.text == "Камчатский край", "Значение CHANGE_REGION не изменилось на 'Камчатский край'"
        assert yar_partners_list != kamch_partners_list, "Список партнеров не изменился"
