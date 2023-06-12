import pytest

from src.classes.work_with_user import WorkWithUser

@pytest.fixture
def get_exmpl_user():
    return WorkWithUser()


def test_check_exit(get_exmpl_user):
    assert get_exmpl_user.check_exit('0') is True
    assert get_exmpl_user.check_exit('1') is False
    assert get_exmpl_user.check_exit('rt') is False


def test_check_entry(get_exmpl_user):
    assert get_exmpl_user.check_entry(1, {1: 10, '2': 15}) is True
    assert get_exmpl_user.check_entry('2', {1: 10, '2': 15}) is True
    assert get_exmpl_user.check_entry(5, {1: 10, '2': 15}) is False
