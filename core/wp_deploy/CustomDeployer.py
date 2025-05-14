from core.wp_deploy.BaseDeployer import BaseWpDeployer


class CustomDeployer(BaseWpDeployer):
    deployer_type = 'Custom'

    def __init__(self,env_path_inside):
        super().__init__()
        self.env_path_inside =''


    def deploy(self):

        print(f'Запуск {self.__class__.deployer_type}')