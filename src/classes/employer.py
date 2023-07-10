class Employer:
    """Класс с набором методов и атрибутов работодателя"""
    __slots__ = ('__employer_id', '__name', '__area')

    def __init__(self, employer_id=None, name=None, area=None):
        self.__employer_id = employer_id
        self.__name = name
        self.__area = area

    @staticmethod
    def get_list_employer(vacancies: list[dict]) -> list:
        """Метод получает список уникальных id работодателей из списка вакансий"""

        employer_ids = set()
        for i in vacancies:
            employer_ids.add(i['employer_id'])
        return list(employer_ids)


