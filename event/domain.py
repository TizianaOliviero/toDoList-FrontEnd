import re

from dataclasses import dataclass, field, InitVar
from datetime import datetime
from typing import List, Union, Any

from typeguard import typechecked
from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Name:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('name', self.value, max_len=50, custom=pattern(r'^[a-zA-Z0-9 ]+$'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Description:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('description', self.value, max_len=500, custom=pattern(r'^[a-zA-Z0-9 ]+$'))

    def __str__(self):
        return self.value


# da controllare
@typechecked
@dataclass(frozen=True, order=True)
class Author:
    key: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('key', self.key)

    def __str__(self):
        return str(self.key)


@typechecked
@dataclass(frozen=True, order=True)
class Date:
    date: datetime

    def __post_init__(self):
        validate_dataclass(self)
        validate('date', self.date, min_value=datetime.now())

    def __str__(self):
        return str(self.date)


@typechecked
@dataclass(frozen=True, order=True)
class Location:
    value: str

    def __post_init__(self, ):
        validate_dataclass(self)
        validate('location', self.value, max_len=50, custom=pattern(r'^[a-zA-Z0-9 ]+$'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Category:
    value: int

    def __post_init__(self, ):
        validate_dataclass(self)
        validate('category', self.value, min_value=0, max_value=3)

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Priority:
    value: int

    def __post_init__(self, ):
        validate_dataclass(self)
        validate('priority', self.value, min_value=0, max_value=2)

    def __str__(self):
        return str(self.value)


@typechecked
@dataclass(frozen=True, order=True)
class Event:
    id:int
    name: Name
    description: Description
    author: Author
    start_date: Date
    end_date: Date
    location: Location
    category: Category
    priority: Priority

    def __str__(self):
        return str('name\t description\t start_date\t end_date\t location\t category\t priority\n' +
                   str(self.name) + '\t' + str(self.description) + '\t' + str(self.start_date) + '\t' + str(
            self.end_date) +
                   '\t' + str(self.location) + '\t' + str(self.category) + '\t' + str(self.priority) + '\n')

    def __post_init__(self, ):
        validate_dataclass(self)
        validate('date', self.end_date, min_value=self.start_date)


@typechecked
@dataclass(frozen=True)
class ToDoList:
    __events: List[Event] = field(default_factory=list, init=False)

    def clear(self):
        self.__events.clear()

    def events(self) -> int:
        return len(self.__events)

    def event(self, index: int):
        validate('index', index, min_value=0, max_value=self.events() - 1)
        return self.__events[index]

    def add_event(self, event: Event) -> None:
        self.__events.append(event)

    def remove_event(self, index: int) -> None:
        validate('index', index, min_value=0, max_value=self.events() - 1)
        del self.__events[index]

    def sort_by_start_date(self) -> None:
        self.__events.sort(key=lambda x: x.start_date)

    def sort_by_priority(self) -> None:
        self.__events.sort(key=lambda x: x.priority, reverse=True)
