import pytest

from src.classes.vacancy import Vacancy


@pytest.fixture
def get_exmpl():
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
    return Vacancy(data[0]), Vacancy(data[1])


def test_init(get_exmpl):
    assert get_exmpl[0].name == "CMM-менеджер"
    assert get_exmpl[0].employer == "ГОУ Научная библиотека Академии государственной службы"
    assert get_exmpl[0].area == "Санкт-Петербург"
    assert get_exmpl[0].url == "https://spb.superjob.ru/vakansii/cmm-menedzher-46528768.html"


def test_get_max_salary(get_exmpl):
    assert get_exmpl[0].get_max_salary(get_exmpl[0], get_exmpl[1]) == (34800, 0)


def test_comparison(get_exmpl):
    assert str(get_exmpl[0] < get_exmpl[1]) == 'False'
    assert str(get_exmpl[0] <= get_exmpl[1]) == 'False'
    assert str(get_exmpl[0] == get_exmpl[1]) == 'False'
    assert str(get_exmpl[0] > get_exmpl[1]) == "True"
    assert str(get_exmpl[0] >= get_exmpl[1]) == 'True'
