import os
import sys
import json
import datetime

__doc__ = "Task Tracker or task-cli is a Command Line Interface program for managing tasks"

time = datetime.datetime.now().strftime("%X %d-%m-%Y")

filename = "storage.json"

class TaskManager:
    """Manages a list of tasks, allowing adding, updating, deleting, marking progress, and listing."""

    def __init__(self, filename):
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
            return

    def _save_data(self):
        """Saves the current list of tasks to the JSON file."""
        with open(self.filename, "w") as f:
            json.dump(self.task_list, f, indent=0)

    def add(self, desc):
        """Adds a new task to the task list.

        Args:
            desc (str): The description of the new task.
        """
        if self.task_list:
            task_id = self.task_list[-1]['id'] + 1
        else:
            task_id = 1

        task = {
            "id": task_id,
            "description": desc,
            "status": "todo",
            "createdAt": time,
            "updatedAt": "",
        }
        self.task_list.append(task)
        self._save_data()
        print(f"Task added successfully (ID: {task_id})")

    def update(self, task_id, desc):
        """Updates the description of a task with the given ID.

        Args:
            task_id (int): The ID of the task to update.
            desc (str): The new description for the task.
        """
        for task in self.task_list:
            if task_id == task['id']:
                print(f"Task {task['id']} - {desc} was updated")
                task['description'] = desc
                task['updatedAt'] = time
                self._save_data()
                return
        print("Task ID not in List")

    def delete(self, task_id):
        """Deletes a task with the given ID from the task list.

        Args:
            task_id (int): The ID of the task to delete.
        """
        for task in self.task_list:
            if task_id == task['id']:
                print(f"Task {task['id']} - {task['description']} was deleted")
                self.task_list.remove(task)
                self._save_data()
                return
        print("Task ID not in List")

    def mark_in_progress(self, task_id):
        """Marks a task with the given ID as 'in-progress'.

        Args:
            task_id (int): The ID of the task to mark.
        """
        for task in self.task_list:
            if task_id == task['id']:
                task["status"] = "in-progress"
                print(f"Task {task_id} status was updated")
                self._save_data()
                return
        print("Task ID not in List")

    def mark_done(self, task_id):
        """Marks a task with the given ID as 'done'.

        Args:
            task_id (int): The ID of the task to mark.
        """
        for task in self.task_list:
            if task_id == task['id']:
                task["status"] = "done"
                print(f"Task {task_id} status was updated")
                self._save_data()
                return
        print("Task ID not in List")

    def list(self, status=""):
        """Lists tasks, optionally filtering by status.

        Args:
            status (str, optional): The status to filter by ('todo', 'in-progress', 'done'). Defaults to "".
        """
        filtered_tasks = [task for task in self.task_list if status == "" or task["status"] == status]

        if not filtered_tasks:
            print("No tasks found.")
            return

        max_id = len("ID")
        max_desc = len("Description")

        # Calculate maximum width for ID and Description
        for task in filtered_tasks:
            id_len = len(str(task["id"]))
            desc_len = len(task["description"])

            if id_len > max_id:
                max_id = id_len
            if desc_len > max_desc:
                max_desc = desc_len

        # Fixed widths for other columns
        status_width = 11
        created_width = 19
        updated_width = 19

        # Calculate total table length
        table_len = max_id + 3 + max_desc + 3 + status_width + 3 + created_width + 3 + updated_width + 2
        print("\n" + "-" * table_len)
        # Print header
        print(f"{'ID':<{max_id}} | {'Description':<{max_desc}} | {'Status':<{status_width}} | {'Created At':<{created_width}} | {'Updated At':<{updated_width}} | ")
        print("-" * table_len)
        # Print tasks
        for task in filtered_tasks:
            print(f"{task['id']:<{max_id}} | {task['description']:<{max_desc}} | {task['status']:<{status_width}} | {task['createdAt']:<{created_width}} | {task['updatedAt']:<{updated_width}} | ")
            print("-" * table_len)

def main():
    """Main function to handle command-line arguments and interact with the TaskManager."""
    task_manager = TaskManager(filename)

    if not os.path.exists(filename):
        task_manager._save_data()  # Create the file if it doesn't exist
    else:
        try:
            task_manager._load_data()  # Load data from the file
        except json.JSONDecodeError:
            print("File was corrupted, a new one will be created")
            task_manager._save_data()  # Create a new file if the existing one is corrupted

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
                task_id = int(sys.argv[2])
                description = sys.argv[3]
                task_manager.update(task_id, description)
            except IndexError:
                print("\nPlease provide an id and a description\n")

        elif command == "delete":
            try:
                task_id = int(sys.argv[2])
                task_manager.delete(task_id)
            except IndexError:
                print("\nPlease provide an id for the task\n")

        elif command == "mark-in-progress":
            try:
                task_id = int(sys.argv[2])
                task_manager.mark_in_progress(task_id)
            except IndexError:
                print("\nPlease provide an id\n")

        elif command == "mark-done":
            try:
                task_id = int(sys.argv[2])
                task_manager.mark_done(task_id)
            except IndexError:
                print("\nPlease provide an id\n")

        elif command == "list":
            try:
                status = sys.argv[2]
                task_manager.list(status)
            except IndexError:
                task_manager.list()
        else:
            print(f"\nCommand {command} not found, please try again!\n")

    except IndexError:
        print("\nPlease provide a command\nUsage: python task-cli.py <command> [arguments]\nCommands:\n    add [Description]\n    update [ID] [Description]\n    delete [ID]\n    mark-done [ID]\n    mark-in-progress [ID]\n    list [status] (if status is empty will return all tasks)")

if __name__ == "__main__":
    main()