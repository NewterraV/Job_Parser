import pytest
from src.classes.working_with_files import WorkingWithJSON, WorkingWithExel
from src.classes.vacancy import Vacancy


@pytest.fixture
def get_exmple():
    return [WorkingWithJSON(), WorkingWithExel()]


def test_check_param(get_exmple):
    data = [{
        "aggregator": "SuperJob",
        "name": "CMM-менеджер",
        "employer": "ГОУ Научная библиотека Академии государственной службы",
        "salary": {
            "from": 0,
            "to": 34800,
            "currency": "rub"
        },
        "area": "Санкт-Петербург",
        "created": "2023-06-06T14:38:28",
        "url": "https://spb.superjob.ru/vakansii/cmm-menedzher-46528768.html",
        "requirement": "Обязанности:\n• Создание макетов информационных материалов (флаеров, стендовых и "
                       "презентационных материалов);\n• Подготовка и обработка"
                       " фотоматериалов;\n• Участие в работе п..."
    },
        {
            "aggregator": "HeadHunter",
            "name": "Программист (PHP/JS/Python)",
            "employer": "МАРКСОФТ",
            "salary": {
                "from": 0,
                "to": 0,
                "currency": None
            },
            "area": "Ижевск",
            "created": "2023-06-05T11:00:50+0300",
            "url": "https://hh.ru/vacancy/81523785",
            "requirement": "Программирование на любом из современных языков (PHP/JS/<highlighttext>"
                           "Python</highlighttext>). Желание обучаться новым технологиям."
        }
    ]
    param = [{'name': 'Программист',
              'salary': None,
              'area': None,
              'keyword': 'Python'},
             {'name': None,
              'salary': [25000, 40000],
              'area': "Санкт-Петербург",
              'keyword': None},
             {'name': None,
              'salary': None,
              'area': None,
              'keyword': "жили-был"},
             {'name': None,
              'salary': None,
              'area': None,
              'keyword': None},
             {'name': None,
              'salary': [250000, 400000],
              'area': None,
              'keyword': None},
             {'name': None,
              'salary': [0, 80000],
              'area': None,
              'keyword': None}
             ]

    assert len(get_exmple[0].get_list_by_param(data, param[0])) == 1
    assert len(get_exmple[0].get_list_by_param(data, param[1])) == 1
    assert len(get_exmple[0].get_list_by_param(data, param[2])) == 0
    assert len(get_exmple[0].get_list_by_param(data, param[2])) == 0
    assert len(get_exmple[0].get_list_by_param(data, param[3])) == 2
    assert len(get_exmple[0].get_list_by_param(data, param[5])) == 2


def test_workingwithjson(get_exmple):
    data = [{
        "aggregator": "SuperJob",
        "name": "CMM-менеджер",
        "employer": "ГОУ Научная библиотека Академии государственной службы",
        "salary": {
            "from": 0,
            "to": 34800,
            "currency": "rub"
        },
        "area": "Санкт-Петербург",
        "created": "2023-06-06T14:38:28",
        "url": "https://spb.superjob.ru/vakansii/cmm-menedzher-46528768.html",
        "requirement": "Обязанности:\n• Создание макетов информационных материалов (флаеров, стендовых и "
                       "презентационных материалов);\n• Подготовка и обработка"
                       " фотоматериалов;\n• Участие в работе п..."
    },
        {
            "aggregator": "HeadHunter",
            "name": "Программист (PHP/JS/Python)",
            "employer": "МАРКСОФТ",
            "salary": {
                "from": 0,
                "to": 0,
                "currency": None
            },
            "area": "Ижевск",
            "created": "2023-06-05T11:00:50+0300",
            "url": "https://hh.ru/vacancy/81523785",
            "requirement": "Программирование на любом из современных языков (PHP/JS/<highlighttext>"
                           "Python</highlighttext>). Желание обучаться новым технологиям."
        }
    ]
    param = {'name': 'Программист',
             'salary': None,
             'area': None,
             'keyword': 'Python'}
    vacancy_1 = Vacancy(data[0])
    vacancy_2 = Vacancy(data[1])

    get_exmple[0].write_file(data)
    get_exmple[0].clear_file_by_param(param)

    get_exmple[1].write_file([vacancy_1, vacancy_2])

