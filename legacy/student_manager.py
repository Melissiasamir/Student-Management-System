# Student Management System
# A simple command-line program to manage student records.

import json
import os

FILE_NAME = "students.json"


# Load students from the JSON file
def load_students():
    # If the file does not exist, start with an empty list
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            content = file.read()
            # If the file is empty, return an empty list
            if content.strip() == "":
                return []
            students = json.loads(content)
            return students
    except (json.JSONDecodeError, IOError):
        # If the file has invalid data or cannot be read, start fresh
        print("Warning: Could not read students.json. Starting with an empty list.")
        return []


# Save students to the JSON file
def save_students(students):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(students, file, indent=4)
    except IOError:
        print("Error: Could not save data to students.json.")


# Add a new student
def add_student(students):
    print("\n--- Add Student ---")
    student_id = input("Enter student ID: ").strip()

    # Check if the ID already exists
    for student in students:
        if student["id"] == student_id:
            print("A student with this ID already exists.")
            return

    name = input("Enter student name: ").strip()

    # Basic error handling for age input
    try:
        age = int(input("Enter student age: "))
    except ValueError:
        print("Invalid age. Age must be a number.")
        return

    grade = input("Enter student grade: ").strip()

    # Create a dictionary for the new student
    new_student = {
        "id": student_id,
        "name": name,
        "age": age,
        "grade": grade
    }

    students.append(new_student)
    save_students(students)
    print("Student added successfully.")


# View all students
def view_students(students):
    print("\n--- All Students ---")

    if len(students) == 0:
        print("No students found.")
        return

    for student in students:
        print("ID: {}, Name: {}, Age: {}, Grade: {}".format(
            student["id"], student["name"], student["age"], student["grade"]
        ))


# Search for a student by ID
def search_student(students):
    print("\n--- Search Student ---")
    student_id = input("Enter student ID to search: ").strip()

    found = False
    for student in students:
        if student["id"] == student_id:
            print("ID: {}, Name: {}, Age: {}, Grade: {}".format(
                student["id"], student["name"], student["age"], student["grade"]
            ))
            found = True
            break

    if not found:
        print("Student not found.")


# Update student information
def update_student(students):
    print("\n--- Update Student ---")
    student_id = input("Enter student ID to update: ").strip()

    for student in students:
        if student["id"] == student_id:
            print("Leave input blank to keep the current value.")

            new_name = input("Enter new name ({}): ".format(student["name"])).strip()
            if new_name != "":
                student["name"] = new_name

            new_age = input("Enter new age ({}): ".format(student["age"])).strip()
            if new_age != "":
                try:
                    student["age"] = int(new_age)
                except ValueError:
                    print("Invalid age. Keeping the previous age.")

            new_grade = input("Enter new grade ({}): ".format(student["grade"])).strip()
            if new_grade != "":
                student["grade"] = new_grade

            save_students(students)
            print("Student updated successfully.")
            return

    print("Student not found.")


# Delete a student
def delete_student(students):
    print("\n--- Delete Student ---")
    student_id = input("Enter student ID to delete: ").strip()

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            save_students(students)
            print("Student deleted successfully.")
            return

    print("Student not found.")


# Main function to run the program
def main():
    # Load existing students when the program starts
    students = load_students()

    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


# Run the program
if __name__ == "__main__":
    main()
