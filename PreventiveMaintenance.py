import datetime
import json

class RepetitiveTask:
    def __init__(self, description, frequency_days, next_execution_date=None):
        self.description = description
        self.frequency_days = frequency_days
        if next_execution_date:
            self.next_execution_date = datetime.date.fromisoformat(next_execution_date)
        else:
            self.next_execution_date = datetime.date.today()

    def __lt__(self, other):
        return self.next_execution_date < other.next_execution_date

    def to_dict(self):
        """Converts the task object to a dictionary for saving."""
        return {
            'description': self.description,
            'frequency_days': self.frequency_days,
            'next_execution_date': self.next_execution_date.isoformat()
        }

    @staticmethod
    def from_dict(data):
        """Creates a task object from a dictionary loaded from a file."""
        return RepetitiveTask(
            data['description'],
            data['frequency_days'],
            data['next_execution_date']
        )
    
    def mark_as_done(self):
        """Updates the task's next due date."""
        self.next_execution_date += datetime.timedelta(days=self.frequency_days)
        print(f"Task '{self.description}' marked as done. Next due date: {self.next_execution_date}")

def save_tasks(todo_list, filename="tasks.json"):
    """Saves the current todo list to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump([task.to_dict() for task in todo_list], f, indent=4)
        print("Tasks saved successfully!")
    except IOError:
        print("Error: Could not save tasks to file.")

def load_tasks(filename="tasks.json"):
    """Loads tasks from a JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return [RepetitiveTask.from_dict(item) for item in data]
    except (IOError, json.JSONDecodeError):
        print("No existing task file found or file is corrupt. Starting with an empty list.")
        return []

def create_task(todo_list):
    """Creates a new repetitive task."""
    description = input("Enter a description for the new task: ")
    while True:
        try:
            frequency = int(input("Enter the frequency in days: "))
            if frequency <= 0:
                print("Frequency must be a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    new_task = RepetitiveTask(description, frequency)
    todo_list.append(new_task)
    todo_list.sort()
    print("New task created successfully!")

def view_tasks(todo_list):
    """Displays the sorted to-do list."""
    if not todo_list:
        print("Your to-do list is empty. Time to create some tasks!")
    else:
        print("\n--- Current To-Do List ---")
        for i, task in enumerate(todo_list):
            print(f"{i+1}. {task.description} (Due: {task.next_execution_date})")
        print("--------------------------\n")

def complete_task(todo_list):
    """Marks a task as done and updates its position."""
    if not todo_list:
        print("No tasks to complete.")
        return

    view_tasks(todo_list)
    while True:
        try:
            task_index = int(input("Enter the number of the task to mark as done: ")) - 1
            if 0 <= task_index < len(todo_list):
                completed_task = todo_list.pop(task_index)
                completed_task.mark_as_done()
                todo_list.append(completed_task)
                todo_list.sort()
                break
            else:
                print("Invalid task number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def delete_task(todo_list):
    """Deletes a task from the list."""
    if not todo_list:
        print("No tasks to delete.")
        return

    view_tasks(todo_list)
    while True:
        try:
            task_index = int(input("Enter the number of the task to delete: ")) - 1
            if 0 <= task_index < len(todo_list):
                deleted_task = todo_list.pop(task_index)
                print(f"Task '{deleted_task.description}' has been deleted.")
                break
            else:
                print("Invalid task number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def edit_task(todo_list):
    """Edits an existing task's description and/or frequency."""
    if not todo_list:
        print("No tasks to edit.")
        return

    view_tasks(todo_list)
    while True:
        try:
            task_index = int(input("Enter the number of the task to edit: ")) - 1
            if 0 <= task_index < len(todo_list):
                task = todo_list[task_index]
                
                new_description = input(f"Enter new description (current: '{task.description}'): ")
                if new_description:
                    task.description = new_description

                new_frequency_str = input(f"Enter new frequency in days (current: {task.frequency_days}): ")
                if new_frequency_str:
                    try:
                        new_frequency = int(new_frequency_str)
                        if new_frequency > 0:
                            task.frequency_days = new_frequency
                        else:
                            print("Frequency must be a positive number. Keeping old value.")
                    except ValueError:
                        print("Invalid input. Keeping old frequency.")
                
                print("Task updated successfully!")
                todo_list.sort() # Re-sort in case the frequency change affects the due date
                break
            else:
                print("Invalid task number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    """Main function to run the preventive maintenance program."""
    todo_list = load_tasks()
    
    while True:
        print("\n--- Preventive Maintenance Program ---")
        print("1. Create a new repetitive task")
        print("2. View all tasks")
        print("3. Mark a task as done")
        print("4. Delete a task")
        print("5. Edit a task")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            create_task(todo_list)
        elif choice == '2':
            view_tasks(todo_list)
        elif choice == '3':
            complete_task(todo_list)
        elif choice == '4':
            delete_task(todo_list)
        elif choice == '5':
            edit_task(todo_list)
        elif choice == '6':
            save_tasks(todo_list)
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option (1-6).")

if __name__ == "__main__":
    main()
