import os

from dotenv import load_dotenv
from injector import Injector

from mircrewapi.client.mircrew_client import MircrewClient
from mircrewapi.logger.app_logger import AppLogger
from mircrewapi.manager.cache_manager import CacheManager


class DefaultContainer:
    """Example dependency container inspired by the coursify layout."""

    injector = None
    instance = None

    @staticmethod
    def getInstance():
        if DefaultContainer.instance is None:
            DefaultContainer.instance = DefaultContainer()
        return DefaultContainer.instance

    def __init__(self):
        self.injector = Injector()

        load_dotenv()

        self._init_environment_variables()
        self._init_directories()
        self._init_logging()
        self._init_bindings()

    def get(self, key):
        return self.injector.get(key)

    def get_var(self, key):
        return self.__dict__[key]

    def _init_directories(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.var_dir = os.path.join(self.root_dir, 'var')
        os.makedirs(self.var_dir, exist_ok=True)
        self.log_dir = os.path.join(self.var_dir, 'log')
        os.makedirs(self.log_dir, exist_ok=True)
        self.app_log_path = os.path.join(self.log_dir, 'app.log')
        self.session_dir = os.path.join(self.root_dir, self.session_dir_env)
        os.makedirs(self.session_dir, exist_ok=True)

    def _init_environment_variables(self):
        self.debug = os.environ.get('DEBUG', 'false').lower() == 'true'
        self.api_host = os.environ.get('API_HOST', '0.0.0.0')
        self.api_port = int(os.environ.get('API_PORT', '8000'))
        self.session_dir_env = os.environ.get('SESSION_DIR', 'var/session')
        self.cache_dir = os.environ.get('CACHE_DIR', 'var/cache')
        self.mircrew_username = os.environ.get('MIRCREW_USERNAME', '')
        self.mircrew_password = os.environ.get('MIRCREW_PASSWORD', '')

    def _init_logging(self):
        AppLogger(self.log_dir, debug=self.debug).configure_root()

    def _init_bindings(self):
        cache_manager = CacheManager(cache_dir=os.path.join(self.root_dir, self.cache_dir))
        self.injector.binder.bind(CacheManager, to=cache_manager)

        mircrew_client = MircrewClient(
            username=self.mircrew_username,
            password=self.mircrew_password,
            cache_manager=cache_manager,
        )
        self.injector.binder.bind(MircrewClient, to=mircrew_client)
