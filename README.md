# Task Tracker CLI

A simple Command Line Interface program for managing tasks.

## Description

This program allows users to add, update, delete, mark the status of tasks (todo, in-progress, done), and list them. The data is stored in a JSON file.

## How to Run the Project

1.  **Make sure you have Python 3 installed on your system.**
2.  **Save the Python code to a file named `task-cli.py` (or any other name you prefer).**
3.  **Open your terminal or command prompt.**
4.  **Navigate to the directory where you saved the Python file.**
5.  **Run the program using the command:**

    ```
    python task-cli.py <command> [arguments]
    ```

## Available Commands

* `add "<description>"`: Adds a new task with the specified description (the description must be enclosed in quotes if it contains spaces).
* `update <id> "<description>"`: Updates the description of the task with the specified ID.
* `delete <id>`: Deletes the task with the specified ID.
* `mark-in-progress <id>`: Marks the task with the specified ID as 'in-progress'.
* `mark-done <id>`: Marks the task with the specified ID as 'done'.
* `list`: Lists all tasks.
* `list <status>`: Lists tasks with the specified status (todo, in-progress, done).

## Notes

* Task data is stored in the `storage.json` file (the filename may vary if you modified it).
* Task IDs are automatically assigned in order.

## Project Page URL

[https://roadmap.sh/projects/task-tracker](https://roadmap.sh/projects/task-tracker)
