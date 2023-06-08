class FileIsEmpty(Exception):

    def __str__(self):
        return Exception('Файл пуст.')
