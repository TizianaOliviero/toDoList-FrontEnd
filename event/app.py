import csv
import json
import sys
import getpass
from datetime import datetime

import requests
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

from event.domain import Name, Description, Author, Date, Priority, Category, Location, Event, ToDoList
from event.menu import Menu, Entry, MenuDescription



class App:
    __filename = Path(__file__).parent.parent / 'default.csv'
    __delimiter = '\t'

    __key = None


    def __real_menu(self):
        self.__menu = Menu.Builder(MenuDescription('To Do List Home'), auto_select=lambda: self.__print_events()) \
            .with_entry(Entry.create('1', 'Add event', on_selected=lambda: self.__add_event())) \
            .with_entry(Entry.create('2', 'Remove event', on_selected=lambda: self.__remove_event())) \
            .with_entry(Entry.create('3', 'Sort by start date', on_selected=lambda: self.__sort_by_start_date())) \
            .with_entry(Entry.create('4', 'Sort by priority', on_selected=lambda: self.__sort_by_priority())) \
            .with_entry(Entry.create('5', 'Print Events', on_selected=lambda: self.__print_events())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()

    def __init__(self):
        self.__real_menu()
        self.__toDoList = ToDoList()

    def __login(self):
        username = input('Username: ')
        password = input('Password: ')

        res = requests.post(url=f'{api_server}/auth/login/', data={'username': username, 'password': password})
        if res.status_code != 200:
            return False
        json = res.json()
        self.__key = json['key']
        return True

    def __registrati(self):
        username = input('Username: ')
        email = input("Email: ")
        password = input('Password: ')
        password2 = input('Ripeti Password: ')

        res = requests.post(url=f'{api_server}/auth/registation/', data={'username': username, 'email': email, 'password': password, 'password2': password2})
        if res.status_code != 200:
            return None
        json = res.json()
        return json['key']

    def __print_events(self) -> None:
        print_sep = lambda: print('-' * 150)
        print_sep()
        fmt = '%20s %30s %5s %20s %20s %20s %10s %10s'
        print(fmt % ('NAME', 'DESCRIPTION', 'AUTHOR', 'START DATE', 'END DATE', 'LOCATION', 'CATEGORY', 'PRIORITY'))
        print_sep()
        self.fetch_posts(self.__key)
        for index in range(self.__toDoList.events()):
            event = self.__toDoList.event(index)
            print(fmt % (event.name.value, event.description.value, event.author.key, event.start_date.date, event.end_date.date, event.location.value, event.category.value, event.priority.value))
        print_sep()

    def __add_event(self) -> None:
        event = Event(*self.__read_event())
        res=requests.post(url=f'{api_server}', json=json.dumps(event))
        self.__toDoList.add_event(event)
        print('Event added!')


    def __remove_event(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__toDoList.events())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return
        todelete=self.__toDoList.event(index-1)
        res=requests.delete(url=f'{api_server}/{todelete.id}')
        self.__toDoList.remove_event(index - 1)
        print('Event removed!' + res)

    def __sort_by_start_date(self) -> None:
        self.__toDoList.sort_by_start_date()


    def __sort_by_priority(self) -> None:
        self.__toDoList.sort_by_priority()


    def fetch_posts(self, key):
        res = requests.get(url=f'{api_server}/events', headers={'Authorization': f'Token {key}'})
        if res.status_code != 200:
            return None
        self.__toDoList.clear()
        json = res.json()
        for item in json:
            id= int(item['id'])
            name = Name(item['name'])
            description = Description(item['description'])
            start_date = Date(datetime.strptime(item['start_date'], '%Y-%m-%dT%H:%M:%SZ'))
            end_date = Date(datetime.strptime(item['end_date'], '%Y-%m-%dT%H:%M:%SZ'))
            location = Location(item['location'])
            category = Category(item['category'])
            priority = Priority(item['priority'])
            self.__toDoList.add_event(Event(id, name, description, Author(1), start_date, end_date, location, category, priority))

        return res.json()

    def __run(self) -> None:
        welcome()

        key = self.__login()

        if key is False:
            error_message()

        self.fetch_posts(self.__key)


        self.__menu.run()
        #show_posts(events)
        #logout(key)
        #goodbye()


    def run(self) -> None:
        #try:
            self.__run()
        #except:
         #   print('Panic error!', file=sys.stderr)



    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                if prompt == "Start date" or prompt == "End date":
                    line = datetime.strptime(line, '%m/%d/%y %H:%M:%S')
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

    def __read_event(self) -> Tuple[int, Name, Description, Date, Date, Location, Category, Priority]:
        name = self.__read('Name', Name)
        description = self.__read('Description', Description)
        start_date = self.__read('Start date', Date)
        end_date = self.__read('End date', Date)
        location = self.__read('Location', Location)
        category = self.__read('Category', Category)
        priority = self.__read('Priority', Priority)
        return -1, name, description, Author(1), start_date, end_date, location, category, priority


#def main(name: str):
 #   if name == '__main__':
  #      App().run()




api_server = 'http://localhost:8000/api/v1'


def main():
    app = App()
    app.run()



def welcome():
    print('============== Blog TUI =============')
    print('= Because we love the \'80s so much! =')
    print('=====================================\n')



def error_message():
    print('Unable to retrieve posts at the moment. Please, try in a few minutes.')
    exit()


def goodbye():
    print('It was nice to have your here. Have a nice day!\n')





def logout(key):
    res = requests.post(url=f'{api_server}/auth/logout/', headers={'Authorization': f'Token {key}'})
    if res.status_code == 200:
        print('Logged out!')
    else:
        print('Log out failed')
    print()





def show_posts(events):
    def sep():
        print('-' * 180)

    fmt = '{:20}\t{:40}\t{:7}\t{:25}\t{:25}\t{:20}\t{:8}\t{:8}'

    print()
    sep()
    print('ALL EVENTS FROM TODOLIST')
    sep()
    print(fmt.format('NAME', 'DESCRIPTION', 'AUTHOR', 'START_DATE', 'END_DATE', 'LOCATION', 'PRIORITY', 'CATEGORY'))
    sep()
    for event in events:
        print(fmt.format(event['name'], event['description'], str(event['author']), event['start_date'], event['end_date'], event['location'], str(event['priority']), str(event['category'])))
    sep()
    print()





main()
