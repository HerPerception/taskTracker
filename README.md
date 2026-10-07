# Task Tracker

A simple command-line interface (CLI) application for efficiently managing and tracking tasks.

This project was built as a solution for the [Task Tracker](https://roadmap.sh/projects/task-tracker) challenge from [roadmap.sh](https://roadmap.sh/).

## Features

* Add new tasks with a unique ID.
* Store tasks in a JSON file.
* List all tasks.
* List tasks by their status: `todo`, `in-progress`, or `done`.
* Update the description of an existing task.
* Delete tasks by their ID.
* Mark tasks as `in-progress` or `done`.

## Prerequisites

* Python 3.12 or newer.
* Git.

## Installation

### Clone the Repository

```bash
git clone https://github.com/HerPerception/taskTracker.git
cd taskTracker
```

### Create a Virtual Environment

```bash
python3 -m venv venv
```

### Activate the Virtual Environment

On Linux/macOS:

```bash
source venv/bin/activate
```

### Install the Project

```bash
pip install -e .
```

After installation, the `task-cli` command will be available while the virtual environment is active.

## Usage

### Add a Task

```bash
task-cli add "Drink a Coffee"
```

### List Tasks

List all tasks:

```bash
task-cli list
```

List only `todo` tasks:

```bash
task-cli list todo
```

List only `in-progress` tasks:

```bash
task-cli list in-progress
```

List only `done` tasks:

```bash
task-cli list done
```

### Update a Task

```bash
task-cli update 1 "Drink a Coffee and Do Coding"
```

### Mark a Task as In Progress

```bash
task-cli mark-in-progress 1
```

### Mark a Task as Done

```bash
task-cli mark-done 1
```

### Delete a Task

```bash
task-cli delete 1
```

## Data Storage

Tasks are stored in a `tasks.json` file.

The file is created in the directory where the command is executed. For example:

```bash
cd my-tasks
task-cli list
```

The application will look for:

```text
my-tasks/tasks.json
```

### Sample JSON Structure

```json
[
  {
    "id": 1,
    "description": "Drink a Coffee",
    "status": "todo"
  }
]
```

## Available Commands

| Command                              | Description                |
| ------------------------------------ | -------------------------- |
| `task-cli add <task>`                | Add a new task             |
| `task-cli list`                      | List all tasks             |
| `task-cli list todo`                 | List todo tasks            |
| `task-cli list in-progress`          | List in-progress tasks     |
| `task-cli list done`                 | List completed tasks       |
| `task-cli update <id> <description>` | Update a task              |
| `task-cli mark-in-progress <id>`     | Mark a task as in progress |
| `task-cli mark-done <id>`            | Mark a task as done        |
| `task-cli delete <id>`               | Delete a task              |
