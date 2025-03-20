import os
import sys
import json
import datetime

__doc__ = "Task Tracker or task-cli is a Comand Line Interface program for managing tasks"

time = datetime.datetime.now().strftime("%d-%m-%Y, %X")

filename = "storage.json"

class TaskManager:
    """Manages a list of tasks, allowing adding, updating, deleting, marking progress, and listing."""
    def __init__ (self, filename):
        """Initializes the TaskManager with the specified filename and loads existing tasks."""
        self.filename = filename
        self.task_list = self._load_data()

    def _load_data(self):
        """Loads task data from the JSON file.

        Returns:
            list: A list of task dictionaries, or an empty list if the file doesn't exist or is corrupted.
        """
        try:
            with open(self.filename) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("File not found or corrupted!")
            return []

    def _save_data(self):
        """Saves the current list of tasks to the JSON file."""
        with open(self.filename, "w") as f:
            json.dump(self.task_list, f)

    def add(self, desc):
        """Adds a new task to the task list.

        Args:
            desc (str): The description of the new task.
        """
        if self.task_list:
            id = self.task_list[-1]['id'] + 1
        else:
            id = 1

        task = {
            "id": id,
            "description": desc,
            "status": "todo",
            "createdAt": time,
            "updatedAt": "",
        }
        self.task_list.append(task)
        self._save_data()
        print(f"Task added successfully (ID: {id})")

    def update(self, id, desc):
        """Updates the description of a task with the given ID.

        Args:
            id (int): The ID of the task to update.
            desc (str): The new description for the task.
        """
        for task in self.task_list:
            if id == task['id']:
                task['description'] = desc
                self._save_data()
                return
        print("Task ID not in List")

    def delete(self, id):
        """Deletes a task with the given ID from the task list.

        Args:
            id (int): The ID of the task to delete.
        """
        for task in self.task_list:
            if id == task['id']:
                self.task_list.remove(task)
                self._save_data()
                return
        print("Task ID not in List")

    def mark_in_progress(self, id):
        """Marks a task with the given ID as 'in-progress'.

        Args:
            id (int): The ID of the task to mark.
        """
        for task in self.task_list:
            if id == task['id']:
                task["status"] = "in-progress"
                print(f"Task {id} status was updated")
                self._save_data()
                return
        print("Task ID not in List")

    def mark_done(self, id):
        """Marks a task with the given ID as 'done'.

        Args:
            id (int): The ID of the task to mark.
        """
        for task in self.task_list:
            if id == task['id']:
                task["status"] = "done"
                print(f"Task {id} status was updated")
                self._save_data()
                return
        print("Task ID not in List")

    def list(self, status = ""):
        """Lists tasks, optionally filtering by status.

        Args:
            status (str, optional): The status to filter by ('todo', 'in-progress', 'done'). Defaults to "".
        """
        for task in self.task_list:
            if status == "": # If no status is provided, list all tasks
                print(task["description"]) # Print only the description
            elif task["status"] == status:
                print(task["description"])

def main():
    """Main function to handle command-line arguments and interact with the TaskManager."""
    task_manager = TaskManager(filename)

    if not os.path.exists(filename):
        task_manager._save_data() # Create the file if it doesn't exist
    else:
        try:
            task_manager._load_data() # Load data from the file
        except json.JSONDecodeError:
            print("File was corrupted, a new one will be created")
            task_manager._save_data() # Create a new file if the existing one is corrupted

    try:
        command = sys.argv[1]

        if command == "add":
            try:
                description = sys.argv[2]
                task_manager.add(description)
            except IndexError:
                print("\nPlease provide a description for the task\n")

        elif command == "update":
            try:
                id = int(sys.argv[2])
                description = sys.argv[3]
                task_manager.update(id, description)
            except IndexError:
                print("\nPlease provide an id and a description\n")

        if command == "delete":
            try:
                id = int(sys.argv[2])
                task_manager.delete(id)
            except IndexError:
                print("\nPlease provide an id for the task\n")

        elif command == "mark-in-progress":
            try:
                id = int(sys.argv[2])
                task_manager.mark_in_progress(id)
            except IndexError:
                print("\nPlease provide an id\n")

        elif command == "mark-done":
            try:
                id = int(sys.argv[2])
                task_manager.mark_done(id)
            except IndexError:
                print("\nPlease provide an id\n")

        elif command == "list":
            try:
                status = sys.argv[2]
                task_manager.list(status)
            except IndexError:
                task_manager.list()

    except IndexError:
        print("\nPlease provice a command\nUsage: python task-cli.py <command> [arguments]\n")

if __name__ == "__main__":
    main()