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


@typechecked
@dataclass(frozen=True, order=True)
class Author:
    key: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('key', self.key)

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Date:
    date: datetime

    def __post_init__(self):
        validate_dataclass(self)
        validate('date', self.date, min_value=datetime.now())

    def __str__(self):
        return self.date



@typechecked
@dataclass(frozen=True, order=True)
class Location:
    value: str

    def __post_init__(self,):
        validate_dataclass(self)
        validate('location', self.value, max_len=50, custom=pattern(r'^[a-zA-Z0-9 ]+$'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True, order=True)
class Event:
    name: Name
    description: Description
    author: Author
    location: Location

    @property
    def type(self) -> str:
        return 'Car'

    @property
    #mettere il check della data


@typechecked
@dataclass(frozen=True)
class ToDoList:
    __events: List[Event] = field(default_factory=list, init=False)

    def vehicles(self) -> int:
        return len(self.__vehicles)

    def vehicle(self, index: int) -> Union[Car, Moto]:
        validate('index', index, min_value=0, max_value=self.vehicles() - 1)
        return self.__vehicles[index]

    def add_car(self, car: Car) -> None:
        self.__vehicles.append(car)

    def add_moto(self, moto: Moto) -> None:
        self.__vehicles.append(moto)

    def remove_vehicle(self, index: int) -> None:
        validate('index', index, min_value=0, max_value=self.vehicles() - 1)
        del self.__vehicles[index]

    def sort_by_producer(self) -> None:
        self.__vehicles.sort(key=lambda x: x.producer)

    def sort_by_price(self) -> None:
        self.__vehicles.sort(key=lambda x: x.price)
