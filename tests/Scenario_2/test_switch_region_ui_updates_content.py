import pytest
from pages.saby_page import SabyPage
from pages.saby_contacts_page import SabyContactsPage

class TestSwitchRegion:
    def test_switch_region_ui_updates_content(self):

        # 1. Переходим на главную страницу
        saby_page = SabyPage(self.driver)
        saby_page.open()

        # 2. Переходим Saby -> Контакты
        contacts_page = saby_page.go_to_contacts()

        # 3. Проверить, что в блоке наш регион и есть список партнеров



        # 4. Изменить регион на Камчатский край через UI

        # 5. Проверить, что подставился регион, список партнёров изменился, url и title содержат информацию региона





