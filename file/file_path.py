import os

from atf import Config

UNIX_BUILDER = ('test-selenium-builder1.unix.tensor.ru', 'test-selenium-builder2.unix.tensor.ru')


class FolderPath(object):

    def __init__(self, relative_path: str):
        """Класс для работы с путями к папкам в тестах!

        :warning сюда необходимо передавать только относительный путь к папке!!!

        :param relative_path - относительный путь к папке
        """
        # на всякий случай, вдруг слэши виндовые
        self._relative_path = relative_path
        self.on_builder = self._relative_path.replace('\\', os.sep)
        self.on_node = self.get_path_on_node()

    def get_path_on_node(self):
        """Отдает путь на ноде, где запущены браузеры"""

        config = Config()
        download_dir_browser = config.get('ETH_DOWNLOAD_DIR_BROWSER') or config.get('eth_download_dir_browser')
        network_path = self.on_builder.replace('/', '\\')
        if download_dir_browser:
            path = '{}\\{}'.format(download_dir_browser, network_path)
        else:
            path = network_path
        return path


class FilePath(object):

    def __init__(self, folder, file):
        self._folder = folder
        self.folder_path = FolderPath(folder)
        self._file = file
        self.on_builder = os.path.join(self.folder_path.on_builder, file)
        self.on_node = '{}\\{}'.format(self.folder_path.on_node, file)


class FolderPathShare(object):

    def __init__(self, relative_path: str):
        """Класс для работы с путями к папкам в тестах!

        :warning сюда необходимо передавать только относительный путь к папке!!!

        :param relative_path - относительный путь к папке
        """

        self._relative_path = relative_path
        config = Config()
        share_dir = config.get('SHARE_DIR')
        if share_dir:
            self.on_builder = os.path.join(share_dir.replace('/', os.sep), self._relative_path)
        else:
            self.on_builder = self._relative_path
        self.on_node = self.get_path_on_node()

    def get_path_on_node(self):
        """Отдает путь на ноде, где запущены браузеры"""

        config = Config()
        share_dir = config.get('SHARE_DIR')
        network_path = self.on_builder
        if share_dir:
            path = os.path.join(config.get('SHARE_DIR_PATH'), self._relative_path)
        else:
            path = network_path
        return path


class FilePathShare(object):

    def __init__(self, folder, file):
        self._folder = folder
        self.folder_path = FolderPathShare(folder)
        self._file = file
        self.on_builder = os.path.join(self.folder_path.on_builder, file)
        self.on_node = '{}\\{}'.format(self.folder_path.on_node, file)