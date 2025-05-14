import os

from core.tools.data_finder.ClassFinder import ClassFinder
from core.tools.data_finder.data_finder import DataFinder as df
from core.tools.file_manager.FileContentManager import FileContentManager
from core.tools.file_manager.file_manager import FileManager
from core.tools.handlers.handler_path import HandlerPath
from core.tools.handlers.handler_request import HandlerRequests
from logger.logger import CustomLogger


class BaseWpDeployer:
    deployer_type = 'Base'
    def __init__(self):


        self.handler_request = HandlerRequests()
        self.handler_path = HandlerPath()
        self.fcontent_manager = FileContentManager()
        self.file_manager = FileManager()
        self.error_log = CustomLogger().error_log


        self.base_dir = self.handler_path.base_dir
        self.template_wp_dir = self.handler_path.find_file(['templates', 'wordpress'], self.base_dir)

        self.path_settings_deploy = self.handler_path.find_file('deploy_config.json', self.base_dir)
        self.settings_deploy = self.file_manager.read_file(self.path_settings_deploy)
        self.settings_deploy_env = df(self.settings_deploy).find('environments')[0]['environments']
        self.env_name = df(self.settings_deploy).find('env_name')[0]['env_name'].lower()
        self.env_path_inside = ''
        self.path_wp_env = ''


    def check_env_name(self,env_path):
        try:
            is_env_name_low = self.handler_path.find_file(self.env_name, env_path)
            is_env_name_cap = self.handler_path.find_file(self.env_name.capitalize(),env_path)
            if is_env_name_low or is_env_name_cap:
                self.env_name+='1'
                self.check_env_name(env_path)
        except Exception as e:
            self.error_log(e)


    def update_wp_template(self):
        try:
            lasted_version, url_download  = self.handler_request.get_wp_version()
            wp_name = url_download[url_download.rfind('/') + 1:]
            wp_folder_name = f'environment_{wp_name}'.replace('.zip','')

            self.path_wp_env = self.handler_path.find_file(wp_folder_name, self.template_wp_dir)
            if not self.path_wp_env or self.fcontent_manager.is_larger_than(self.path_wp_env,102400, True):
                self.fcontent_manager.delete_path(self.template_wp_dir, starts_with = 'environment_wordpress')
                self.path_wp_env = self.fcontent_manager.create_folder(self.template_wp_dir, wp_folder_name)
                self.handler_request.download_and_extract(url_download,self.path_wp_env)
                self.error_log('Актуальну версію WordPress встановлено!')
            else:
                self.error_log('Уже встановлена актуальна версія WordPress')

        except Exception as e:
            self.error_log(e)


    def deploy(self):
        self.update_wp_template()

        class_finder = ClassFinder(self.handler_path.base_dir,'BaseWpDeployer' )
        child_classes = class_finder.find_child_class()
        for env in self.settings_deploy_env:
            if env['isProcess']:
                env_type = env['type']
                env_path = env['path']
                self.check_env_name(env_path)
                self.env_path_inside = self.fcontent_manager.create_folder(env_path, self.env_name.capitalize())
                self.fcontent_manager.copy_files(self.path_wp_env,self.env_path_inside)
                for c_cls in child_classes:
                    if c_cls.deployer_type == env_type:
                        c_cls(self.env_path_inside).deploy()
                        pass


if __name__ == '__main__':
    bd = BaseWpDeployer()
    bd.deploy()