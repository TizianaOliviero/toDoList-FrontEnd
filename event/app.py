import csv
import sys
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

from event.domain import Name, Description, Author, Date, Priority, Category, Location, Event, ToDoList
from event.menu import Menu, Entry, Description



class App:
    __filename = Path(__file__).parent.parent / 'default.csv'
    __delimiter = '\t'

    def __init__(self):
        self.__menu = Menu.Builder(Description('To Do List Home'), auto_select=lambda: self.__print_events())\
            .with_entry(Entry.create('1', 'Add event', on_selected=lambda: self.__add_event()))\
            .with_entry(Entry.create('2', 'Remove event', on_selected=lambda: self.__remove_event()))\
            .with_entry(Entry.create('3', 'Sort by srart date', on_selected=lambda: self.__sort_by_start_date()))\
            .with_entry(Entry.create('4', 'Sort by priority', on_selected=lambda: self.__sort_by_priority()))\
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True))\
            .build()
        self.__toDoList = ToDoList()

    def __print_events(self) -> None:
        print_sep = lambda: print('-' * 100)
        print_sep()
        fmt = '%30s %-30s %-3s %-30s %30s %30s %3 %3'
        print(fmt % ('NAME', 'DESCRIPTION', 'AUTHOR', 'START DATE', 'END DATE', 'LOCATION', 'CATEGORY', 'PRIORITY'))
        print_sep()
        for index in range(self.__toDoList.events()):
            event = self.__toDoList.event(index)
            print(fmt % (index + 1, event.name.value, event.description.value, event.author.key, event.start_date.date, event.end_date.date, event.location.value, event.category.value, event.priority.value))
        print_sep()

    def __add_event(self) -> None:
        event = Event(*self.__read_event())
        self.__toDoList.add_event(event)
        self.__save()
        print('Event added!')


    def __remove_event(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__toDoList.events())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return
        self.__toDoList.remove_event(index - 1)
        self.__save()
        print('Vehicle removed!')

    def __sort_by_start_date(self) -> None:
        self.__toDoList.sort_by_start_date()
        self.__save()

    def __sort_by_priority(self) -> None:
        self.__toDoList.sort_by_priority()
        self.__save()

    def __run(self) -> None:
        try:
            self.__load()
        except ValueError as e:
            print(e)
            print('Continuing with an empty list of events...')

        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)

    def __load(self) -> None:
        pass



    def __save(self) -> None:
        pass

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __read_event(self) -> Tuple[Name, Description, Date, Date, Location, Category, Priority]:
        name = self.__read('Name', Name)
        description = self.__read('Description', Description)
        start_date = self.__read('Start date', Date)
        end_date = self.__read('End date', Date)
        location = self.__read('Location', Location)
        category = self.__read('Category', Category)
        priority = self.__read('Priority', Priority)
        return name, description, start_date, end_date, location, category, priority


def main(name: str):
    if name == '__main__':
        App().run()

main(__name__)
