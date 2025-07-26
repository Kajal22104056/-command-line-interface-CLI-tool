# 📝 Task Manager CLI Tool

A command-line interface (CLI) utility to manage your tasks efficiently with support for **priority levels**, **due dates**, **search**, and **persistent storage**.

---

## 🚀 Features

- **Add Tasks**: Include optional priority (`Low`, `Medium`, `High`) and due dates.
- **Color-Coded Display**:
  - High → 🔴 Red  
  - Medium → 🟡 Yellow  
  - Low → 🟢 Green
- **List Tasks**: View pending tasks; use `--show-completed` to include completed ones.
- **Complete Tasks**: Mark tasks as finished.
- **Delete Tasks**: Remove tasks from either the pending or completed list.
- **Search Tasks**: Search task descriptions using keywords.
- **Prioritize**: Sort tasks by priority and due date.
- **Persistent Storage**: Saves all tasks in `tasks.txt` for use across sessions.

---

## ⚙️ Installation

Ensure you have **Python** installed. Then:

1. Clone the repository or download the script.
2. Navigate to the script directory in your terminal.

---

## 🧪 Usage

Run the tool using the following format:

```bash
python <script_name>.py <command> [options]
Replace <script_name> with the actual name of your Python script (e.g., task_manager.py).
