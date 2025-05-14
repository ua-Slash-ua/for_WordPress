import os
import shutil
import zipfile

from core.tools.data_finder.data_finder import DataFinder as Df
from core.tools.file_manager.file_manager import FileManager
from core.tools.handlers.handler_path import HandlerPath
from logger.logger import CustomLogger
import requests
import json

class HandlerRequests:
    def __init__(self):
        self.error_log = CustomLogger().error_log

        self.handle_path = HandlerPath()
        self.file_manager = FileManager()
        self.path_settings_hr = self.handle_path.find_file('hr_config.json',self.handle_path.base_dir)
        self.settings_hr = self.file_manager.read_file(self.path_settings_hr)

        self.data_founder = Df(self.settings_hr).find

    def get_wp_version(self):
        """
        :return: version, url_download
        """
        try:
            url = self.data_founder('wordpress_version', 0)
            response = requests.get(url)
            response.raise_for_status()  # підніме виняток, якщо код відповіді не 200
            data = response.json()  # замість json.loads(response.text)

            offer = data.get('offers', [{}])[0]
            version = offer.get('version')
            url_download = offer.get('download')
            if version and url_download:
                self.settings_hr['wordpress_download'] = url_download
                self.file_manager.write_file(self.path_settings_hr, self.settings_hr)
                self.error_log(f'Остання версія Wordpress < {version} >, оновлено посилання для скачування архіву')
                return version, url_download
            else:
                self.error_log('Не вдалося знайти версію або посилання на завантаження в JSON-відповіді.')
                return None
        except (requests.RequestException, json.JSONDecodeError) as e:
            self.error_log(f'Помилка при отриманні версії WordPress: {e}')
            return None

    def download_and_extract(self, url_download: str, folder_path: str):
        """
        Скачування архіву та його розархівовування без вкладеної папки 'wordpress'.

        :param url_download: URL для скачування архіву
        :param folder_path: Папка, куди потрібно розпакувати вміст
        """
        try:
            self.error_log(f'Завантаження архіву з {url_download}...')
            response = requests.get(url_download, stream=True)
            response.raise_for_status()

            zip_path = os.path.join(folder_path, 'wordpress.zip')
            with open(zip_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            self.error_log(f'Архів скачано до {zip_path}')

            # Тимчасова папка для розпакування
            temp_extract_path = os.path.join(folder_path, '__temp_wordpress_extract__')
            os.makedirs(temp_extract_path, exist_ok=True)

            self.error_log(f'Розархівування в тимчасову папку {temp_extract_path}...')
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_path)

            wordpress_dir = os.path.join(temp_extract_path, 'wordpress')
            if not os.path.isdir(wordpress_dir):
                raise Exception('У архіві не знайдено папки "wordpress".')

            # Перенесення вмісту з 'wordpress' до folder_path
            for item in os.listdir(wordpress_dir):
                src_path = os.path.join(wordpress_dir, item)
                dst_path = os.path.join(folder_path, item)

                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)

            self.error_log(f'Архів успішно розархівовано в {folder_path}')

            # Очистка
            os.remove(zip_path)
            shutil.rmtree(temp_extract_path)
            self.error_log(f'Тимчасовий архів та розпаковані файли видалено')

        except requests.RequestException as e:
            self.error_log(f'Помилка при завантаженні архіву: {e}')
        except zipfile.BadZipFile as e:
            self.error_log(f'Пошкоджений ZIP-архів: {e}')
        except Exception as e:
            self.error_log(f'Неочікувана помилка: {e}')


if __name__ == '__main__':
    hr = HandlerRequests()
    hr.get_wp_version()