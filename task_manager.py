import os
import argparse
from datetime import datetime

# Constants for file path
TASK_FILE = "tasks.txt"

def load_tasks():
    """Load tasks from file into a dictionary of pending and completed tasks."""
    tasks = {"pending": [], "completed": []}
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("[Completed]"):
                    task_data = line.replace("[Completed] ", "").split(" | ")
                    tasks["completed"].append({"description": task_data[0], "priority": task_data[1], "due_date": task_data[2]})
                else:
                    task_data = line.split(" | ")
                    tasks["pending"].append({"description": task_data[0], "priority": task_data[1], "due_date": task_data[2]})
    return tasks

def save_tasks(tasks):
    """Save tasks to a .txt file with specific formatting for completed and pending tasks."""
    with open(TASK_FILE, "w") as file:
        for task in tasks["pending"]:
            file.write(f"{task['description']} | {task['priority']} | {task['due_date']}\n")
        for task in tasks["completed"]:
            file.write(f"[Completed] {task['description']} | {task['priority']} | {task['due_date']}\n")

def add_task(tasks, task_description, priority="Low", due_date="No Due Date"):
    """Add a new task with optional priority and due date."""
    task = {
        "description": task_description,
        "priority": priority.capitalize(),
        "due_date": due_date
    }
    tasks["pending"].append(task)
    print(f"Task '{task_description}' added with priority '{priority}' and due date '{due_date}'.")

def view_tasks(tasks, show_completed=False):
    """Display pending and optionally completed tasks with color coding."""
    def colored(text, color):
        colors = {"red": "\033[91m", "yellow": "\033[93m", "green": "\033[92m", "end": "\033[0m"}
        return f"{colors.get(color, colors['end'])}{text}{colors['end']}"

    print("\nPending Tasks:")
    if not tasks["pending"]:
        print("No pending tasks.")
    else:
        for idx, task in enumerate(tasks["pending"], 1):
            color = {"High": "red", "Medium": "yellow", "Low": "green"}.get(task["priority"], "end")
            print(f"{idx}. {colored(task['description'], color)} - Priority: {task['priority']}, Due: {task['due_date']}")

    if show_completed:
        print("\nCompleted Tasks:")
        if not tasks["completed"]:
            print("No completed tasks.")
        else:
            for idx, task in enumerate(tasks["completed"], 1):
                print(f"{idx}. {task['description']} - Completed")

def mark_task_complete(tasks, task_num):
    """Mark a task from the pending list as completed."""
    if 1 <= task_num <= len(tasks["pending"]):
        task = tasks["pending"].pop(task_num - 1)
        tasks["completed"].append(task)
        print(f"Task '{task['description']}' marked as completed.")
    else:
        print("Invalid task number. Please enter a valid number.")

def delete_task(tasks, task_num, from_completed=False):
    """Delete a task from pending or completed list."""
    try:
        if from_completed:
            task = tasks["completed"].pop(task_num - 1)
            print(f"Task '{task['description']}' deleted from completed tasks.")
        else:
            task = tasks["pending"].pop(task_num - 1)
            print(f"Task '{task['description']}' deleted from pending tasks.")
    except IndexError:
        print("Invalid task number.")

def prioritize_tasks(tasks):
    """Sort tasks by priority and due date."""
    priority_map = {"High": 1, "Medium": 2, "Low": 3}
    tasks["pending"].sort(
        key=lambda t: (
            priority_map.get(t["priority"], 4), 
            t["due_date"] if t["due_date"] != "No Due Date" else "9999-12-31"
        )
    )
    print("Pending tasks sorted by priority and due date.")

def search_tasks(tasks, keyword):
    """Search tasks by keyword."""
    print("\nSearch Results:")
    found = False
    for category in ["pending", "completed"]:
        for idx, task in enumerate(tasks[category], 1):
            if keyword.lower() in task["description"].lower():
                print(f"{category.capitalize()} Task {idx}: {task['description']} - Priority: {task['priority']}, Due: {task['due_date']}")
                found = True
    if not found:
        print("No tasks found matching the keyword.")

def main():
    """Main function to handle command-line arguments and perform operations."""
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add task
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", type=str, help="Task description")
    parser_add.add_argument("--priority", choices=["low", "medium", "high"], default="low",
                           help="Priority of the task. Options: low, medium, high. Default is low.")
    parser_add.add_argument("--due-date", type=str, help="Optional due date in YYYY-MM-DD format.")

    # List tasks
    parser_list = subparsers.add_parser("list", help="List tasks")
    parser_list.add_argument("--show-completed", action="store_true", help="Show completed tasks")

    # Complete task
    parser_complete = subparsers.add_parser("complete", help="Mark a task as completed")
    parser_complete.add_argument("task_num", type=int, help="Task number to mark as completed")

    # Delete task
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("task_num", type=int, help="Task number to delete")
    parser_delete.add_argument("--completed", action="store_true", help="Delete from completed tasks")

    # Search tasks
    parser_search = subparsers.add_parser("search", help="Search tasks by keyword")
    parser_search.add_argument("keyword", type=str, help="Keyword to search in tasks")

    # Sort tasks
    subparsers.add_parser("prioritize", help="Sort pending tasks by priority and due date")

    # Parse arguments
    args = parser.parse_args()
    tasks = load_tasks()

    # Perform the command
    if args.command == "add":
        add_task(tasks, args.description, args.priority, args.due_date)
        save_tasks(tasks)
    elif args.command == "list":
        view_tasks(tasks, show_completed=args.show_completed)
    elif args.command == "complete":
        mark_task_complete(tasks, args.task_num)
        save_tasks(tasks)
    elif args.command == "delete":
        delete_task(tasks, args.task_num, from_completed=args.completed)
        save_tasks(tasks)
    elif args.command == "search":
        search_tasks(tasks, args.keyword)
    elif args.command == "prioritize":
        prioritize_tasks(tasks)
        save_tasks(tasks)
    else:
        print("Please specify a valid command. Use '-h' or '--help' for usage information.")
        parser.print_help()

if __name__ == "__main__":
    main()
