from datetime import datetime

import pytest
from dataclass_type_validator import TypeValidationError
from valid8 import ValidationError

from event.domain import Name, Description, Author, Date, Priority, Category, Location, Event, ToDoList


def test_name_format():
    wrong_values = ['', 'a#bcde', '-@#', 'A'*51]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Name(value)

    correct_values = ['CA220NE', 'ABCDE', 'A'*10]
    for value in correct_values:
        assert Name(value).value == value


def test_name_str():
    for value in ['CA220NE', 'ABCDE', 'A'*10]:
        assert str(Name(value)) == value


def test_description_format():
    wrong_values = ['', 'a@', 'a#bcde.', 'AA000bb!', 'A'*501]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Description(value)

    correct_values = ['appuntamento con Ciccio Pasticcio', 'VW', 'A'*100]
    for value in correct_values:
        assert Description(value).value == value


def test_producer_str():
    for value in ['appuntamento con Ciccio Pasticcio', 'VW', 'A'*100]:
        assert str(Description(value)) == value


def test_location_format():
    wrong_values = ['', '$', 'ab@cde.', 'AA000bb!', 'A'*51]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Location(value)

    correct_values = ['Pasticciopoli', 'via ponte bucci', 'A'*50]
    for value in correct_values:
        assert Location(value).value == value


def test_location_str():
    for value in ['Pasticciopoli', 'via ponte bucci', 'A'*50]:
        assert str(Location(value)) == value


def test_wrong_date():
    date=datetime(2010,9,9)
    with pytest.raises(ValidationError):
        Date(date)


def test_wrong_start_end_date():
    start_date = datetime(2021, 9, 9)
    end_date = datetime(2021, 8, 8)
    with pytest.raises(ValidationError):
        Event(Name('nome'), Description('descr'), Author(0), Date(start_date), Date(end_date), Location('casa mia'), Category(1), Priority(1))


def test_category_out_of_range():
    with pytest.raises(ValidationError):
        Category(8)

def test_category_str():

    assert str(Category(2))=='2'

def test_category_wrong_value():
    with pytest.raises(TypeError):
        Category('sdfgh')

def test_priority_out_of_range():
    with pytest.raises(ValidationError):
        Category(8)

def test_priority_str():
    assert str(Priority(2))=='2'

def test_priority_wrong_value():
    with pytest.raises(TypeError):
        Category('sdfgh')

def test_author_str():
    assert str(Author(7))=='7'

def test_add_event():
    toDoList = ToDoList()
    end_date = datetime(2021, 9, 9)
    start_date = datetime(2021, 8, 8)
    event= Event(Name('nome'), Description('descr'), Author(0), Date(start_date), Date(end_date), Location('casa mia'), Category(1), Priority(1))
    toDoList.add_event(event)
    assert toDoList.events()==1

def test_remove_event():
    toDoList = ToDoList()
    end_date = datetime(2021, 9, 9)
    start_date = datetime(2021, 8, 8)
    event= Event(Name('nome'), Description('descr'), Author(0), Date(start_date), Date(end_date), Location('casa mia'), Category(1), Priority(1))
    toDoList.add_event(event)
    toDoList.remove_event(0)
    assert toDoList.events()==0

def test_index_todolist():
    toDoList = ToDoList()
    end_date = datetime(2021, 9, 9)
    start_date = datetime(2021, 8, 8)
    event = Event(Name('nome'), Description('descr'), Author(0), Date(start_date), Date(end_date), Location('casa mia'),
                  Category(1), Priority(1))
    toDoList.add_event(event)
    assert toDoList.event(0)==event

def test_sort_date():
    toDoList = ToDoList()
    end_date = datetime(2021, 9, 9)
    start_date = datetime(2021, 8, 8)
    event = Event(Name('nome'), Description('descr'), Author(0), Date(start_date), Date(end_date), Location('casa mia'),
                  Category(1), Priority(1))
    toDoList.add_event(event)
    start_date2 = datetime(2021, 7, 7)
    event2 = Event(Name('nome'), Description('descr'), Author(0), Date(start_date2), Date(end_date), Location('casa mia'),
                  Category(1), Priority(1))
    toDoList.add_event(event2)
    toDoList.sort_by_start_date()
    assert toDoList.event(0)==event2

def test_sort_priority():
    toDoList = ToDoList()
    end_date = datetime(2021, 9, 9)
    start_date = datetime(2021, 8, 8)
    event = Event(Name('nome'), Description('descr'), Author(0), Date(start_date), Date(end_date), Location('casa mia'),
                  Category(1), Priority(2))
    toDoList.add_event(event)
    start_date2 = datetime(2021, 7, 7)
    event2 = Event(Name('nome'), Description('descr'), Author(0), Date(start_date2), Date(end_date), Location('casa mia'),
                  Category(1), Priority(1))
    toDoList.add_event(event2)
    toDoList.sort_by_priority()
    assert toDoList.event(0)==event

def test_event_str():
    end_date = datetime(2021, 9, 9)
    start_date = datetime(2021, 8, 8)
    event = Event(Name('nome'), Description('descr'), Author(0), Date(start_date), Date(end_date), Location('casa mia'),
                  Category(1), Priority(1))
    print(event)

    assert str(event)=='name\t description\t start_date\t end_date\t location\t category\t priority\n'+ str(event.name) + '\t' + str(event.description) +'\t' + str(event.start_date) + '\t' + str(event.end_date) +'\t' + str(event.location) + '\t' + str(event.category) + '\t' + str(event.priority) + '\n'