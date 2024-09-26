from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QDir, QFileInfo

class Worker(QObject):
    # Создаем сигнал для передачи результата
    result_ready = pyqtSignal(float)

    def __init__(self, directory):
        super().__init__()
        self.directory = directory

    @pyqtSlot()  # Отмечаем как слот, который будет выполняться в потоке
    def run(self):
        # Длительный процесс вычисления размера папки
        size = self.dirSize(self.directory)
        self.result_ready.emit(size)  # Передаем результат через сигнал

    def dirSize(self, dirPath: str):
            """ Подсчет размера папки """
            size_path = 0
            dir = QDir(dirPath)
            for file_path in dir.entryList(QDir.Files | QDir.Hidden):
                    size_path += QFileInfo(dir, file_path).size()
            for child_dir_path in dir.entryList(QDir.Dirs | QDir.NoDotAndDotDot | QDir.Hidden):
                    size_path += self.dirSize(dirPath + QDir.separator() + child_dir_path)
            return size_path