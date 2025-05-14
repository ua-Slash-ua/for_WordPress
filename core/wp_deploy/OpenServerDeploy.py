import os
from typing import List

import psutil

from core.wp_deploy.BaseDeployer import BaseWpDeployer



class OpenServerDeployer(BaseWpDeployer):
    deployer_type = 'OpenServer'


    def __init__(self,env_path_inside):
        super().__init__()
        self.program_name ='ospanel'
        self.os_process = ['ospanel', 'mysqld.exe', 'msedgewebview2.exe', 'httpd.exe']
        self.env_path_inside = env_path_inside

    @staticmethod
    def is_program_running(name: str) -> bool:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and name.lower() in proc.info['name'].lower():
                return True
        return False
    @staticmethod
    def kill_program(os_process: List[str]) -> int:
        killed_count = 0
        targets = [name.lower() for name in os_process]

        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info.get('name', '')
                if proc_name and any(target in proc_name.lower() for target in targets):
                    proc.kill()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        return killed_count

    def create_ini(self):
        path_to_osp = self.fcontent_manager.create_folder(self.env_path_inside, '.osp')
        path_to_ini = os.path.join(path_to_osp,'project.ini')
        try:
            data = f'''[{self.env_name}]

php_engine = PHP-8.3'''
            self.file_manager.write_file(path_to_ini,data)
        except Exception as e:
            self.error_log(e)

    def deploy(self):
        self.error_log(f'Запуск {self.__class__.deployer_type}')
        try:
            self.create_ini()
            parent_dir = os.path.dirname(os.path.dirname(self.env_path_inside))
            bin_dir = self.handler_path.find_file('bin',parent_dir)
            program_path = os.path.join(bin_dir, f'{self.os_process[0]}')
            if self.is_program_running(self.os_process[0]):
                self.kill_program(self.os_process)
            os.startfile(program_path)
            self.error_log(f'Середовище {self.env_name} на базі  {self.__class__.deployer_type} розгорнуто')
        except Exception as e:
            self.error_log(e)

