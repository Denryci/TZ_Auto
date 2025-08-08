import os
import time
import logging
from pathlib import Path
from pages.saby_page import SabyPage

DOWNLOAD_DIR = "./tests/Scenario_3"
EXPECTED_FILE_NAME = "saby-setup.exe"
EXPECTED_FILE_SIZE_MB = 6.02
ALLOWED_SIZE_DEVIATION_MB = 0.1

class TestSabyDownload:
    def _wait_for_download_complete(self, file_path, timeout=60):
        start_time = time.time()
        end_time = start_time + timeout

        # Ждем появления файла
        while not os.path.exists(file_path) and time.time() < end_time:
            time.sleep(1)

        if not os.path.exists(file_path):
            raise TimeoutError(f"Файл не появился за {timeout} секунд")

        # Ждем завершения загрузки (размер перестает меняться)
        stable_size = 0
        stable_count = 0
        while time.time() < end_time:
            try:
                current_size = os.path.getsize(file_path)
                if current_size == stable_size:
                    stable_count += 1
                else:
                    stable_size = current_size
                    stable_count = 0

                # Если размер не менялся 3 секунды подряд - считаем загрузку завершенной
                if stable_count >= 3:
                    return

                # Если файл пустой, ждем начала загрузки
                if current_size == 0:
                    time.sleep(1)
                    continue

                time.sleep(1)
            except OSError:
                # Файл может быть временно недоступен (например, записывается)
                time.sleep(1)

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:
            raise TimeoutError("Файл скачан, но его размер 0 MB")

    def test_download_saby_web_installer_6_02mb(self):
        # 1. Перейдём на главную страницу
        saby_page = SabyPage(self.driver)
        saby_page.open()

        # 2. Переходим на страницу скачивания
        download_page = saby_page.go_to_download()

        # Устанавливаем директорию для загрузки (абсолютный путь)
        abs_download_dir = os.path.abspath(DOWNLOAD_DIR)
        download_page.set_download_directory(abs_download_dir)

        # 3. Нажимаем на кнопку загрузки
        download_page.file_download()

        # Ожидаем скачивание файла
        file_path = os.path.join(DOWNLOAD_DIR, EXPECTED_FILE_NAME)
        self._wait_for_download_complete(file_path)

        # 4. Проверяем что файл существует, имеет правильное расширение и размер
        assert os.path.exists(file_path), f'Файл {EXPECTED_FILE_NAME} не был скачан'

        file_name = Path(file_path).stem  # Получаем имя файла без расширения
        assert file_name == "saby-setup", f'Имя файла "{file_name}", ожидалось "saby-setup"'

        file_extension = Path(file_path).suffix.lower()
        assert file_extension == ".exe", f'Файл имеет расширение {file_extension}, ожидалось .exe'

        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        assert abs(file_size_mb - EXPECTED_FILE_SIZE_MB) <= ALLOWED_SIZE_DEVIATION_MB, f'Размер файла {file_size_mb:.2f} MB, ожидалось {EXPECTED_FILE_SIZE_MB} MB'

        # 5. Удаляем файл после проверки
        os.remove(file_path)

        # 5*. Удаляем вспомогательные ненужные файлы (downloads.htm и +.crdownload)
        for filename in os.listdir(DOWNLOAD_DIR):
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            if filename == "downloads.htm" or filename.endswith(".crdownload"):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Не удалось удалить файл {filename}: {e}")
