import json
import os

class TodoManager:
    def __init__(self, filename='todos.json'):
        self.filename = filename
        self.todos = self.load_todos()

    def load_todos(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            return json.load(file)

    def save_todos(self):
        with open(self.filename, 'w') as file:
            json.dump(self.todos, file, indent=2)

    def add_todo(self, task):
        self.todos.append({'task': task, 'done': False})
        self.save_todos()

    def complete_todo(self, index):
        if 0 <= index < len(self.todos):
            self.todos[index]['done'] = True
            self.save_todos()

    def list_todos(self):
        for idx, todo in enumerate(self.todos):
            status = "✓" if todo['done'] else "✗"
            print(f"{idx+1}. [{status}] {todo['task']}")

if __name__ == "__main__":
    manager = TodoManager()
    while True:
        print("\n1. Add Task  2. Mark Complete  3. List Tasks  4. Exit")
        choice = input("Choose: ")
        if choice == '1':
            task = input("Task: ")
            manager.add_todo(task)
        elif choice == '2':
            index = int(input("Task number to mark complete: ")) - 1
            manager.complete_todo(index)
        elif choice == '3':
            manager.list_todos()
        elif choice == '4':
            break