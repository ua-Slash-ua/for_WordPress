import re
from core.tools.file_manager.file_manager import FileManager
from core.tools.handlers.handler_path import HandlerPath
from logger.logger import CustomLogger


class WpConfigEditor:
    def __init__(self, path_to_wp_config):
        self.path_to_wp_config = path_to_wp_config

        self.handler_path = HandlerPath()
        self.file_manager = FileManager()
        self.error_log = CustomLogger().error_log
        self.template_wp_dir = self.handler_path.find_file(['templates', 'wordpress'], self.handler_path.base_dir)

        self.path_to_template_wp_config = self.handler_path.find_file('data_wp_config.txt', self.template_wp_dir)

    def __get_data_wp_config(self, init_phrase):
        try:
            data_wp_debug = self.file_manager.read_file(self.path_to_template_wp_config)

            index_start = data_wp_debug.find(init_phrase) + len(init_phrase)
            relative_index = data_wp_debug[index_start:].find('/***/')
            index_end = relative_index + index_start if relative_index != -1 else len(data_wp_debug)
            data = data_wp_debug[index_start:index_end].split('\n')
            data = [i.strip() for i in data if i.strip()]

            if len(data) == 1 :
                return data[0]

            return data
        except Exception as e:
            self.error_log(e)
            return []

    def __get_wp_config_index(self, data,  start_phrase, end_phrase, reverse = False):
        try:
            index_start = data.find(start_phrase)
            if reverse:
                index_end = index_start
                index_start = data[:index_end].rfind(end_phrase) + len(end_phrase)
            else:
                index_start += len(start_phrase)
                index_end = data[index_start:].find(end_phrase) + index_start
            return index_start,index_end
        except Exception as e:
            self.error_log(e)
            return None


    def edit_wp_debug(self):
        try:
            start_phrase = f'/* Add any custom values between this line and the "stop editing" line. */'
            end_phrase = f'*/'
            data_wp_config = self.file_manager.read_file(self.path_to_wp_config)
            index_start, index_end = self.__get_wp_config_index(data_wp_config, start_phrase, end_phrase, True)
            data = self.__get_data_wp_config('DATA_WP_DEBUG')

            new_data = data_wp_config[:index_start] + '\n'*2 +'\n'.join(data) + '\n'*2 + data_wp_config[index_end:]
            self.file_manager.write_file(self.path_to_wp_config, new_data)
            self.error_log(f'DEDUG в < wp-config.php > включено!')
        except Exception as e:
            self.error_log(e)



if __name__ == '__main__':
    ce = WpConfigEditor(r'D:\Programms\OSPanel\home\Bilobrov\wp-config.php')
    ce.edit_wp_debug()
