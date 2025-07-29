import csv
import json
import os

# Task storage
tasks = {}

# Load tasks from a file (if it exists)
def load_tasks():
    if os.path.exists('tasks.csv'):
        with open('tasks.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 4:
                    continue
                try:
                    task_id = int(row[0])
                    description = row[1]
                    status = row[2]
                    priority = row[3]
                    tasks[task_id] = {'description': description, 'status': status, 'priority': priority}
                except ValueError:
                    print(f"Skipping invalid row: {row}")
                    continue

# Save tasks to a file
def save_tasks():
    with open('tasks.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for task_id, task in tasks.items():
            writer.writerow([task_id, task['description'], task['status'], task['priority']])

# Function to add a new task
def add_task():
    task_id = max(tasks.keys(), default=0) + 1  # Create a new ID based on the current highest ID
    description = input("Enter task description: ")
    status = input("Enter task status (New, In Progress, Complete): ").capitalize()
    priority = input("Enter task priority (Low, Medium, High): ").capitalize()

    tasks[task_id] = {
        'description': description,
        'status': status,
        'priority': priority
    }

    print(f"Task {task_id} added successfully.")

# Function to list all tasks
def list_tasks():
    if tasks:
        print("\nCurrent Tasks:")
        for task_id, task in tasks.items():
            print(f"ID: {task_id}, Description: {task['description']}, Status: {task['status']}, Priority: {task['priority']}")
    else:
        print("No tasks available.")

# Function to filter tasks by status
def filter_tasks_by_status():
    status = input("\nEnter the status to filter by (New, In Progress, Complete): ").capitalize()
    filtered_tasks = {task_id: task for task_id, task in tasks.items() if task['status'] == status}
    
    if filtered_tasks:
        print(f"\nTasks with status '{status}':")
        for task_id, task in filtered_tasks.items():
            print(f"ID: {task_id}, Description: {task['description']}, Status: {task['status']}, Priority: {task['priority']}")
    else:
        print(f"No tasks found with the status '{status}'.")

# Function to sort tasks (by priority or task ID)
def sort_tasks():
    print("\nHow would you like to sort the tasks?")
    print("1: By Task ID")
    print("2: By Priority (Low, Medium, High)")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == '1':
        sorted_tasks = sorted(tasks.items(), key=lambda x: x[0])  # Sort by Task ID
    elif choice == '2':
        priority_order = {'Low': 1, 'Medium': 2, 'High': 3}
        sorted_tasks = sorted(tasks.items(), key=lambda x: priority_order.get(x[1]['priority'], 0))  # Sort by Priority
    else:
        print("Invalid choice.")
        return

    print("\nSorted Tasks:")
    for task_id, task in sorted_tasks:
        print(f"ID: {task_id}, Description: {task['description']}, Status: {task['status']}, Priority: {task['priority']}")

# Function to edit an existing task
def edit_task():
    task_id = int(input("\nEnter the Task ID to edit: "))
    if task_id not in tasks:
        print("Task ID not found.")
        return

    print(f"Editing Task {task_id}")
    description = input(f"Current Description: {tasks[task_id]['description']}. Enter new description (or press Enter to keep): ")
    if description:
        tasks[task_id]['description'] = description
    
    status = input(f"Current Status: {tasks[task_id]['status']}. Enter new status (New, In Progress, Complete, or press Enter to keep): ")
    if status:
        tasks[task_id]['status'] = status.capitalize()

    priority = input(f"Current Priority: {tasks[task_id]['priority']}. Enter new priority (Low, Medium, High, or press Enter to keep): ")
    if priority:
        tasks[task_id]['priority'] = priority.capitalize()

    print(f"Task {task_id} updated successfully.")

# Function to delete an existing task
def delete_task():
    task_id = int(input("\nEnter the Task ID to delete: "))
    if task_id in tasks:
        del tasks[task_id]
        print(f"Task {task_id} deleted successfully.")
    else:
        print("Task ID not found.")

# Export tasks to CSV file
def export_to_csv():
    with open('tasks.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for task_id, task in tasks.items():
            writer.writerow([task_id, task['description'], task['status'], task['priority']])
    print("Tasks exported to tasks.csv")

# Export tasks to text file
def export_to_txt():
    with open('tasks.txt', mode='w') as file:
        for task_id, task in tasks.items():
            file.write(f"ID: {task_id}, Description: {task['description']}, Status: {task['status']}, Priority: {task['priority']}\n")
    print("Tasks exported to tasks.txt")

# Export tasks to JSON file
def export_to_json():
    with open('tasks.json', 'w') as json_file:
        json.dump(tasks, json_file, indent=4)
    print("Tasks exported to tasks.json")

# Import tasks from CSV file
def import_from_csv(file_name):
    if not os.path.exists(file_name):
        print(f"The file {file_name} does not exist.")
        return
    
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 4:
                continue
            try:
                task_id = int(row[0])
                description = row[1]
                status = row[2]
                priority = row[3]
                tasks[task_id] = {'description': description, 'status': status, 'priority': priority}
            except ValueError:
                print(f"Skipping invalid row: {row}")
                continue

# Import tasks from text file
def import_from_txt(file_name):
    if not os.path.exists(file_name):
        print(f"The file {file_name} does not exist.")
        return
    
    with open(file_name, mode='r') as file:
        for line in file:
            parts = line.strip().split(", ")
            if len(parts) < 4:
                continue
            task_id = int(parts[0].split(": ")[1])
            description = parts[1].split(": ")[1]
            status = parts[2].split(": ")[1]
            priority = parts[3].split(": ")[1]
            tasks[task_id] = {'description': description, 'status': status, 'priority': priority}

# Import tasks from JSON file
def import_from_json(file_name):
    if not os.path.exists(file_name):
        print(f"The file {file_name} does not exist.")
        return

    with open(file_name, 'r') as json_file:
        imported_tasks = json.load(json_file)
        for task_id, task in imported_tasks.items():
            tasks[task_id] = task

# Display the main menu
def display_menu():
    print("\nWelcome to Task Manager")
    print("\033[92m")  # Green text
    print("Press the 1 key for task actions (Add, Edit, Delete)")
    print("Press the 2 key for task listing (List, Filter, Sort)")
    print("Press the 3 key to export tasks")
    print("Press the 4 key to import tasks")
    print("Press the 5 key to exit the program")
    print("\033[0m")  # Reset text color

# Task action sub-menu (Add, Edit, Delete)
def task_action_menu():
    action = input("\nWould you like to 'add', 'edit', or 'delete' a task? (type 'add', 'edit', or 'delete'): ").strip().lower()
    
    if action == 'add':
        add_task()  # Call the add_task function here
    elif action == 'edit':
        edit_task()
    elif action == 'delete':
        delete_task()
    else:
        print("Invalid option. Please type 'add', 'edit', or 'delete'.")

# Task listing sub-menu (List, Filter, Sort)
def task_listing_menu():
    action = input("\nWould you like to 'list', 'filter', or 'sort' tasks? (type 'list', 'filter', or 'sort'): ").strip().lower()

    if action == 'list':
        list_tasks()
    elif action == 'filter':
        filter_tasks_by_status()
    elif action == 'sort':
        sort_tasks()
    else:
        print("Invalid option. Please type 'list', 'filter', or 'sort'.")

# Export tasks sub-menu
def export_task_menu():
    print("\nSelect export format:")
    print("1: CSV")
    print("2: Text")
    print("3: JSON")
    format_choice = input("Choose an option (1-3): ")

    if format_choice == '1':
        export_to_csv()
    elif format_choice == '2':
        export_to_txt()
    elif format_choice == '3':
        export_to_json()
    else:
        print("Invalid option!")

# Import tasks sub-menu
def import_task_menu():
    print("\nSelect import format:")
    print("1: CSV")
    print("2: Text")
    print("3: JSON")
    format_choice = input("Choose an option (1-3): ")

    file_name = input("Enter the filename: ")

    if format_choice == '1':
        import_from_csv(file_name)
    elif format_choice == '2':
        import_from_txt(file_name)
    elif format_choice == '3':
        import_from_json(file_name)
    else:
        print("Invalid option!")

# Main program loop
def main():
    load_tasks()
    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == '1':
            task_action_menu()  # Open the task action sub-menu
        elif choice == '2':
            task_listing_menu()  # Open the task listing sub-menu
        elif choice == '3':
            export_task_menu()  # Open export menu
        elif choice == '4':
            import_task_menu()  # Open import menu
        elif choice == '5':
            save_tasks()
            print("Exiting program...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
