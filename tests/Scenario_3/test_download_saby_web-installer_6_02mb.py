import os
import time
import pytest
from pathlib import Path
from pages.saby_page import SabyPage

DOWNLOAD_DIR = "./tests/Scenario_3"
EXPECTED_FILE_NAME = "saby-setup.exe"
EXPECTED_FILE_SIZE_MB = 6.02
ALLOWED_SIZE_DEVIATION_MB = 1

class TestSabyDownload:
    def _wait_for_download_complete(self, file_path, timeout=30):
        end_time = time.time() + timeout
        while not os.path.exists(file_path) or time.time() < end_time:
            time.sleep(1)

        if not os.path.exists(file_path):
            raise TimeoutError(f"Файл не был скачан за {timeout} секунд")

        # Дополнительная проверка, что файл закончил скачиваться
        file_size = -1
        while time.time() < end_time:
            current_size = os.path.getsize(file_path)
            if current_size == file_size:
                return
            file_size = current_size
            time.sleep(1)

        raise TimeoutError(f"Файл не завершил скачивание за {timeout} секунд")

    def test_download_saby_web_installer_6_02mb(self):
        # 1. Перейдём на главную страницу
        saby_page = SabyPage(self.driver)
        saby_page.open()

        # 2. Переходим на страницу скачивания
        download_page = saby_page.go_to_download()

        # У становим директорию для загрузки
        download_page.set_download_directory(os.path.abspath(DOWNLOAD_DIR))

        # 3. Нажимаем на кнопку загрузки
        download_page.file_download()

        # Ожидаем скачивание файла
        file_path = os.path.join(DOWNLOAD_DIR, EXPECTED_FILE_NAME)
        self._wait_for_download_complete(file_path)

        # 4. Проверяем что файл существует, имеет правильное расширение и размер
        assert os.path.exists(file_path), f'Файл {EXPECTED_FILE_NAME} не был скачан'

        file_extension = Path(file_path).suffix.lower()
        assert file_extension == ".exe", f'Файл имеет расширение {file_extension}, ожидалось .exe'

        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        assert abs(file_size_mb - EXPECTED_FILE_SIZE_MB) <= ALLOWED_SIZE_DEVIATION_MB, f'Размер файла {file_size_mb:.2f} MB, ожидалось {EXPECTED_FILE_SIZE_MB} MB'

        # 5. Удаляем файл после проверки
        os.remove(file_path)