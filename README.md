# Student Management System

## Project Description

The Student Management System is a simple command-line application built in Python. It allows users to manage student records, including adding, viewing, searching, updating, and deleting students. All data is stored persistently in a JSON file, so records are not lost when the program is closed.

This project is designed to demonstrate core Python programming concepts such as variables, conditions, loops, functions, lists, dictionaries, file handling, and basic error handling.

## Features

- Add a new student
- View all students
- Search for a student by ID
- Update student information
- Delete a student
- Automatically save data to `students.json`
- Automatically load data from `students.json` when the program starts

## Project Structure

```
Student-Management-System/
│── main.py
│── students.json
│── README.md
```

- **main.py** — Contains all the program logic and functions.
- **students.json** — Stores student records in JSON format.
- **README.md** — Documentation for the project.

## Requirements

- Python 3.x
- No external libraries required (only built-in `json` and `os` modules are used)

## How to Run the Project

1. Make sure Python 3 is installed on your system.
2. Download or clone this project folder.
3. Open a terminal in the project directory.
4. Run the following command:

```
python main.py
```

5. Follow the on-screen menu to manage student records.

## Example Menu

```
===== Student Management System =====
1. Add Student
2. View All Students
3. Search Student by ID
4. Update Student
5. Delete Student
6. Exit
Enter your choice (1-6):
```

## Student Data Format

Each student record contains the following fields:

```json
{
    "id": "101",
    "name": "Ahmed",
    "age": 20,
    "grade": "A"
}
```
