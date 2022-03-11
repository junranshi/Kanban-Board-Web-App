# Flask Kanban Board
A Kanban Board for managing your to-do lists

## Features

- Add new todo items
- Change item status (todo, doing, done)
- Delete items

## Installation

Install necessary dependencies
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 app.py
```

Your Kanban board should be up and running at http://127.0.0.1:5000/

## Unit Testing

On the project root directory, run
```
$ python3 -m unittest discover test
```
