import json
import os

FILENAME = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""

    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return[]

def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=2)

def add_task(tasks):
    text = input("Enter task: ").strip()

    if not text:
        print("Task can't be empty.\n")
        return
    
    task = {"text": text, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added: \"{text}\"\n")

def view_task(tasks):
    if not tasks:
        print("No tasks yet. Add one!\n")
        return
    
    print("\n Your To-Do List:")
    print("-" * 40)

    for i, task in enumerate(tasks, start=1):
        status = "✔" if task["done"] else " "
        print(f" {i}. [{status}] {task['text']}")

    done_count = len([t for t in tasks if t["done"]])
    print(f"\n {done_count}/{len(tasks)} completed\n")

def complete_task(tasks):
    view_task(tasks)
    if not tasks:
        return
    
    try:
        num = int(input("Task number to complete: "))

        if 1 <= num <= len(tasks):
            tasks[num - 1]["done"] = True
            save_tasks(tasks)
            print(f"Completed: \"{tasks[num - 1]['text']}\"\n")
        else:
            print("Invalid tasks number.\n")
    except ValueError:
        print("Please enter a number.\n")

def delete_task(tasks):
    view_task(tasks)
    if not tasks:
        return
    
    try:
        num = int(input("Task number to delete: "))

        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            save_tasks(tasks)
            print(f"Deleted: \"{removed['text']}\"\n")
        else:
            print("Invalid task number.\n")

    except ValueError:
        print("Please enter a number.\n")

def clear_completed(tasks):
    remaining = [t for t in tasks if not t["done"]]
    removed_count = len(tasks) - len(remaining)

    if removed_count == 0:
        print("No completed tasks to clear.\n")
        return
    
    tasks[:] = remaining
    save_tasks(tasks)
    print(f"Cleared {removed_count} completed tasks(s).\n")

def show_menu():
    print("What would you like to do?")
    print("1. View tasks")
    print("2. Add task")
    print("3. Complete task")
    print("4. Delete task")
    print("5. Clear completed")
    print("6. Quit")

def main():
    print("=" * 40)
    print("To-Do List App")
    print("=" * 40)
    print()

    tasks = load_tasks()

    actions = {
        "1": view_task,
        "2": add_task,
        "3": complete_task,
        "4": delete_task,
        "5": clear_completed
    }

    while True:
        show_menu()
        choice = input("\nChoose (1-6): ").strip()

        if choice == "6":
            print("\nGoodbye!\n")
            break
        
        action = actions.get(choice)
        
        if action:
            action(tasks)
        else:
            print("Please choose 1-6.\n")

if __name__ == "__main__":
    main()