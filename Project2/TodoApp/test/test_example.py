import pytest

# pytest will run all functions with "test" in the name in files with "test" in the name


def test_pass():
    assert 3 == 3
    assert isinstance('ssss', str)
    assert isinstance('10', int) is False
    

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'cs', 3)

def test_person_init(default_employee):
    assert default_employee.first_name == 'John', 'first name should be John'
    assert default_employee.last_name == 'Doe', 'last name should be Doe'
    assert default_employee.major == 'cs', 'major should be cs'
    assert default_employee.years == 3, 'years should be 3'