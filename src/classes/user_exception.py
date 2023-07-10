class FileIsEmpty(Exception):

    def __str__(self):
        return Exception('Файл пуст.')


class CheckExit(Exception):

    def __str__(self):
        return Exception('Exit')
