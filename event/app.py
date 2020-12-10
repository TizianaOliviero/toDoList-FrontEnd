import sys
from datetime import datetime

import requests
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

from event.domain import Name, Description, Author, Date, Priority, Category, Location, Event, ToDoList
from event.menu import Menu, Entry, MenuDescription


api_server = 'http://localhost:8000/api/v1'


class App:
    __filename = Path(__file__).parent.parent / 'default.csv'
    __delimiter = '\t'

    __key = None
    __is_logged = False

    def __first_menu(self):
        self.__first_menu = Menu.Builder(MenuDescription('To Do List Login'), auto_select=lambda: self.__print_events()) \
            .with_entry(Entry.create('1', 'Login', is_logged=lambda: self.__login())) \
            .with_entry(Entry.create('2', 'Sign in', on_selected=lambda: self.__registrati())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()


    def __real_menu(self):
        self.__menu = Menu.Builder(MenuDescription('To Do List Home'), auto_select=lambda: self.__print_events()) \
            .with_entry(Entry.create('1', 'Add event', on_selected=lambda: self.__add_event())) \
            .with_entry(Entry.create('2', 'Remove event', on_selected=lambda: self.__remove_event())) \
            .with_entry(Entry.create('3', 'Sort by start date', on_selected=lambda: self.__sort_by_start_date())) \
            .with_entry(Entry.create('4', 'Sort by priority', on_selected=lambda: self.__sort_by_priority())) \
            .with_entry(Entry.create('5', 'Print Events', on_selected=lambda: self.__print_events())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: self.logout(), is_exit=True)) \
            .build()

    def __init__(self):
        self.__first_menu()
        self.__real_menu()
        self.__toDoList = ToDoList()

    def __login(self):
        self.username = input('Username: ')
        password = input('Password: ')

        res = requests.post(url=f'{api_server}/auth/login/', data={'username': self.username, 'password': password})
        if res.status_code != 200:
            return False
        json = res.json()
        self.__key = json['key']
        print(self.__key)
        res2 = requests.get(url=f'{api_server}/author/{self.username}',headers={'Authorization': f'Token {self.__key}'})
        resString= str(res2.content)
        self.__authorID = int(resString[8:-2])

        return True

    def __registrati(self):
        username = input('Username: ')
        email = input("Email: ")
        password = input('Password: ')
        password2 = input('Ripeti Password: ')

        res = requests.post(url=f'{api_server}/auth/registration/', data={'username': username, 'email': email, 'password1': password, 'password2': password2})
        #print(res.json())
        if res.status_code == 400:
            print('This user already exists!')

    def __print_events(self) -> None:
        print_sep = lambda: print('-' * 150)
        print_sep()
        fmt = '%20s %30s %5s %20s %20s %20s %10s %10s'
        print(fmt % ('NAME', 'DESCRIPTION', 'AUTHOR', 'START DATE', 'END DATE', 'LOCATION', 'CATEGORY', 'PRIORITY'))
        print_sep()
        for index in range(self.__toDoList.events()):
            event = self.__toDoList.event(index)
            print(fmt % (event.name.value, event.description.value, event.author.key, event.start_date.date, event.end_date.date, event.location.value, event.category.value, event.priority.value))
        print_sep()




    def __add_event(self) -> None:
        name, description, start_date, end_date, location, category, priority = self.__read_event()
        print(self.__authorID)
        event = Event(-1,name,description, Author(self.__authorID), start_date, end_date, location, category, priority)
        self.__toDoList.add_event(event)
        obj={
            "name": str(name),
            "description": str(description),
            "author": self.__authorID,
            "start_date": str(start_date),
            "end_date": str(end_date.date),
            "location": str(location),
            "priority": str(category),
            "category": str(priority)
        }

        res = requests.post(url=f'{api_server}/', json=obj,headers={'Authorization': f'Token {self.__key}'});
        self.__toDoList.clear()
        self.fetch_events()
        print('Event added!')

    def __remove_event(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__toDoList.events())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return
        todelete = self.__toDoList.event(index-1)
        res = requests.delete(url=f'{api_server}/{todelete.id}/', headers={'Authorization': f'Token {self.__key}'})
        self.__toDoList.remove_event(index-1)

    def __sort_by_start_date(self) -> None:
        self.__toDoList.sort_by_start_date()

    def __sort_by_priority(self) -> None:
        self.__toDoList.sort_by_priority()


    def fetch_events(self):
        res = requests.get(url=f'{api_server}/events', headers={'Authorization': f'Token {self.__key}'})
        if res.status_code != 200:
            return None

        json = res.json()
        for item in json:
            id = int(item['id'])
            name = Name(item['name'])
            description = Description(item['description'])
            author =Author(item['author'])
            start_date = Date(datetime.strptime(item['start_date'], '%Y-%m-%dT%H:%M:%SZ'))
            end_date = Date(datetime.strptime(item['end_date'], '%Y-%m-%dT%H:%M:%SZ'))
            location = Location(item['location'])
            category = Category(item['category'])
            priority = Priority(item['priority'])
            self.__toDoList.add_event(Event(id,name, description, author, start_date, end_date, location, category, priority))

        return res.json()

    def __run(self) -> None:
        welcome()
        while not self.__first_menu.run() == (True, False):

            if self.__key is False:
                error_message()

            self.fetch_events()
            self.__menu.run()

        goodbye()


    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)


    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                if prompt == "Start date" or prompt == "End date":
                    line = datetime.strptime(line, '%m/%d/%yT%H:%M:%SZ')
                    res = builder(line)
                    return res
                if prompt == "Category" or prompt == "Priority":
                    line = int(line)
                    res = builder(line)
                    return res
                else:
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

    def logout(self):
        res = requests.post(url=f'{api_server}/auth/logout/', headers={'Authorization': f'Token {self.__key}'})
        if res.status_code == 200:
            print('Logged out!')
        else:
            print('Log out failed')
        print()
        self.__key = None
        self.__toDoList.clear()


def main():
    app = App()
    app.run()


def welcome():
    print('================================================================================= ToDoList TUI ===============================================================================')
    print('=================================================================== Because we love the \'80s so much! =======================================================================')
    print('============================================================================================================================================================================\n')


def error_message():
    print('Unable to retrieve events at the moment. Please, try in a few minutes.')
    exit()


def goodbye():
    print('It was nice to have your here. Have a nice day!\n')

main()