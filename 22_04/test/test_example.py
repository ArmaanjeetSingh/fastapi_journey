import pytest
# def test_equal_or_not_equal():
#     assert 3==3

# def test_equal_or_not_equal():
#     assert 3==2

# def test_equal_or_not_equal():
#     assert 3 != 1

# def test_equal_or_not_equal():
#     assert 3 != 3


def test_isInstance():
    assert isinstance('this is string',str)
    assert not isinstance('10',int)

def test_boolean():
    validated = True
    assert validated is True
    assert ("hello" == "world") is not True

def test_list():
    nums = [1,2,3,6,7,8]
    anyList = [False, False]
    assert 1 in nums
    assert 5 not in nums
    assert all(nums)
    assert not any(anyList)


def test_greater_less_than():
    assert 7 > 3
    assert 5 < 9

class Student :
    def __init__(self,first_name : str, last_name : str,major : str, years : int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student("John","Doe","Computer Science",3)

def test_person_intianlization(default_employee):
    assert default_employee.first_name == 'John'
    assert default_employee.last_name == 'Doe'
    assert default_employee.major == 'Computer Science'
    assert default_employee.years == 3