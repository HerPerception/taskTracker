import unittest
import json
import os
import tempfile
import io
from contextlib import redirect_stdout

import helper


class TestTaskTracker(unittest.TestCase):

    def setUp(self):
        # Create a temporary JSON file for each test
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w",
            delete=False
        )

        self.temp_file.write("[]")
        self.temp_file.close()

        # Save the original filename
        self.original_file = helper.FILENAME

        # Make the helper functions use the temporary file
        helper.FILENAME = self.temp_file.name

    def tearDown(self):
        # Restore the original filename
        helper.FILENAME = self.original_file

        # Remove the temporary file
        os.remove(self.temp_file.name)

    def read_tasks(self):
        with open(self.temp_file.name, "r") as file:
            return json.load(file)

    # -------------------------
    # add_task
    # -------------------------

    def test_add_task(self):
        helper.add_task(["Buy groceries"])

        tasks = self.read_tasks()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Buy groceries")
        self.assertEqual(tasks[0]["status"], "todo")

    def test_add_task_has_required_properties(self):
        helper.add_task(["Buy groceries"])

        task = self.read_tasks()[0]

        self.assertIn("id", task)
        self.assertIn("description", task)
        self.assertIn("status", task)
        self.assertIn("createdAt", task)
        self.assertIn("updatedAt", task)

    def test_add_multiple_tasks_have_unique_ids(self):
        helper.add_task(["Buy groceries"])
        helper.add_task(["Clean room"])

        tasks = self.read_tasks()

        self.assertNotEqual(
            tasks[0]["id"],
            tasks[1]["id"]
        )

    # -------------------------
    # update_task
    # -------------------------

    def test_update_task(self):
        helper.add_task(["Buy groceries"])

        task = self.read_tasks()[0]

        helper.update_task([
            str(task["id"]),
            "Buy groceries and cook dinner"
        ])

        tasks = self.read_tasks()

        self.assertEqual(
            tasks[0]["description"],
            "Buy groceries and cook dinner"
        )

    def test_update_task_preserves_id(self):
        helper.add_task(["Buy groceries"])

        task = self.read_tasks()[0]
        task_id = task["id"]

        helper.update_task([
            str(task_id),
            "Cook dinner"
        ])

        updated_task = self.read_tasks()[0]

        self.assertEqual(
            updated_task["id"],
            task_id
        )

    def test_update_task_preserves_created_at(self):
        helper.add_task(["Buy groceries"])

        task = self.read_tasks()[0]
        created_at = task["createdAt"]

        helper.update_task([
            str(task["id"]),
            "Cook dinner"
        ])

        updated_task = self.read_tasks()[0]

        self.assertEqual(
            updated_task["createdAt"],
            created_at
        )

    # -------------------------
    # delete_task
    # -------------------------

    def test_delete_task(self):
        helper.add_task(["Task one"])
        helper.add_task(["Task two"])

        tasks = self.read_tasks()

        helper.delete_task([
            str(tasks[0]["id"])
        ])

        remaining_tasks = self.read_tasks()

        self.assertEqual(len(remaining_tasks), 1)
        self.assertEqual(
            remaining_tasks[0]["description"],
            "Task two"
        )

    def test_delete_task_does_not_delete_other_tasks(self):
        helper.add_task(["Task one"])
        helper.add_task(["Task two"])

        tasks = self.read_tasks()
        task_two_id = tasks[1]["id"]

        helper.delete_task([
            str(tasks[0]["id"])
        ])

        remaining_tasks = self.read_tasks()

        self.assertEqual(
            remaining_tasks[0]["id"],
            task_two_id
        )

    # -------------------------
    # list_tasks
    # -------------------------

    def test_list_all_tasks(self):
        helper.add_task(["Task one"])
        helper.add_task(["Task two"])

        output = io.StringIO()

        with redirect_stdout(output):
            helper.list_tasks([])

        result = output.getvalue()

        self.assertIn("Task one", result)
        self.assertIn("Task two", result)

    def test_list_done_tasks(self):
        helper.add_task(["Task one"])
        helper.add_task(["Task two"])

        tasks = self.read_tasks()

        helper.change_task_status(
            [str(tasks[0]["id"])],
            "mark-done"
        )

        output = io.StringIO()

        with redirect_stdout(output):
            helper.list_tasks(["done"])

        result = output.getvalue()

        self.assertIn("Task one", result)
        self.assertNotIn("Task two", result)

    def test_list_in_progress_tasks(self):
        helper.add_task(["Task one"])
        helper.add_task(["Task two"])

        tasks = self.read_tasks()

        helper.change_task_status(
            [str(tasks[0]["id"])],
            "mark-in-progress"
        )

        output = io.StringIO()

        with redirect_stdout(output):
            helper.list_tasks(["in-progress"])

        result = output.getvalue()

        self.assertIn("Task one", result)
        self.assertNotIn("Task two", result)

    def test_list_todo_tasks(self):
        helper.add_task(["Task one"])
        helper.add_task(["Task two"])

        tasks = self.read_tasks()

        helper.change_task_status(
            [str(tasks[0]["id"])],
            "mark-done"
        )

        output = io.StringIO()

        with redirect_stdout(output):
            helper.list_tasks(["todo"])

        result = output.getvalue()

        self.assertIn("Task two", result)
        self.assertNotIn("Task one", result)

    # -------------------------
    # change_task_status
    # -------------------------

    def test_change_task_status_to_done(self):
        helper.add_task(["Finish project"])

        task = self.read_tasks()[0]

        helper.change_task_status(
            [str(task["id"])],
            "mark-done"
        )

        updated_task = self.read_tasks()[0]

        self.assertEqual(
            updated_task["status"],
            "done"
        )

    def test_change_task_status_to_in_progress(self):
        helper.add_task(["Work on project"])

        task = self.read_tasks()[0]

        helper.change_task_status(
            [str(task["id"])],
            "mark-in-progress"
        )

        updated_task = self.read_tasks()[0]

        self.assertEqual(
            updated_task["status"],
            "in-progress"
        )

    def test_change_task_status_only_changes_selected_task(self):
        helper.add_task(["Task one"])
        helper.add_task(["Task two"])

        tasks = self.read_tasks()

        helper.change_task_status(
            [str(tasks[0]["id"])],
            "mark-done"
        )

        updated_tasks = self.read_tasks()

        self.assertEqual(
            updated_tasks[0]["status"],
            "done"
        )

        self.assertEqual(
            updated_tasks[1]["status"],
            "todo"
        )


if __name__ == "__main__":
    unittest.main()

# python -m unittest test_helper.py


