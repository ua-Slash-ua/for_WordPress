import datetime
import os
import sys
import traceback
from colorama import init, Fore

# Ініціалізація colorama з автоскріпленням
init(autoreset=True)


class CustomLogger:
    def __init__(self):

        self.file_debug = 'debug.log'
        self.file_logging = 'logging.log'

        self.script_dir = self.__get_script_dir()

    @staticmethod
    def __get_script_dir():
        """Повертає директорію, де знаходиться скрипт."""
        return os.path.dirname(os.path.abspath(__file__))

    def __write_file(self, file_name, data='', ftype='a+'):
        full_path_to_file = os.path.join(self.script_dir, file_name)

        try:
            # Відкриваємо файл у потрібному режимі
            with open(full_path_to_file, ftype, encoding='utf-8') as file:
                if data:
                    file.write(f'{data}\n')
        except Exception as e:
            # Логування помилки з деталями
            print(f"❌ Помилка при записі в файл: {full_path_to_file}")
            print(f"Технічна деталь: {e}")

            # Виведення детальної інформації про помилку (стек трейс)
            print("Трасування помилки:")
            traceback.print_exc()

    def __print_data(self, cs_data, current_status):
        if cs_data:
            if current_status == '[Error]':  # Якщо статус помилки
                print(Fore.RED + f'Сталася помилка перевірте < {self.file_debug} >')
            elif current_status == '[DON’T forget]':
                print(Fore.CYAN + f'Не забудьте оновити дані, перегляньте  < {self.file_logging} > із статусом {current_status} >')
            elif current_status == '[Warning]':
                print(Fore.YELLOW + f'Попередження, перегляньте  < {self.file_debug} > із статусом {current_status} >')
            elif current_status == '[Unknown]':
                print(Fore.RED + f'Невідомий статус, перегляньте  < {self.file_logging} > із статусом {current_status} >')


    def error_log(self, msg, status='info'):
        all_status = {
            'info': {'name': 'Info', 'isLog': True, 'isDebug': False, 'isPrint': False},
            'err': {'name': 'Error', 'isLog': False, 'isDebug': True, 'isPrint': True},
            'war': {'name': 'Warning', 'isLog': False, 'isDebug': True, 'isPrint': True},
            'exist': {'name': 'Already exist', 'isLog': True, 'isDebug': False, 'isPrint': False},
            'forget': {'name': 'DON’T forget', 'isLog': True, 'isDebug': False, 'isPrint': True},
            'Unknown': {'name': 'Unknown', 'isLog': True, 'isDebug': False, 'isPrint': True},
        }

        # Якщо повідомлення є виключенням, змінюємо статус на 'err'
        if isinstance(msg, Exception):
            status = 'err'

            # Отримуємо деталі помилки
            exc_type, exc_value, exc_tb = sys.exc_info()  # Отримуємо інформацію про виключення
            error_details = traceback.format_exception(exc_type, exc_value, exc_tb)

            # Формуємо рядок помилки
            err_msg = f"File: {error_details[-2].strip()},\n Error: {str(msg)}"
            msg = err_msg

        # Вибір поточного статусу
        current_status = f'[{all_status.get(status, all_status["Unknown"])["name"]}]'
        cs_data = all_status.get(status, all_status["Unknown"])

        # Отримуємо поточний час
        time_now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        time_now = f'[{time_now.strip()}]'

        full_msg = ''.join([time_now, current_status, ' ', msg])

        self.__print_data(cs_data['isPrint'], current_status)

        if cs_data['isDebug']:
            self.__write_file(self.file_debug, full_msg)
        if cs_data['isLog']:
            self.__write_file(self.file_logging, full_msg)

        # Виведення логів
        # print(time_now)
        # print(current_status)
        # print(cs_data)


if __name__ == '__main__':
    s = CustomLogger()
    s.error_log('Wellcome')
    try:
        a = 1 / 0
    except Exception as e:
        s.error_log(e)
