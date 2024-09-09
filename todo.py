import typer

app = typer.Typer()
# A list to store tasks
tasks = []
@app.command()
def add_task(task: str):
    """Add a new task to the to-do list."""
    tasks.append({"task": task, "completed": False})
    typer.echo(f"Task '{task}' added to the to-do list.")
@app.command()
def list_tasks(show_completed: bool = False):
    """List all tasks in the to-do list."""
    if not tasks:
        typer.echo("No tasks in the to-do list.")
    else:
        typer.echo("To-Do List:")
        for i, task in enumerate(tasks, start=1):
            if show_completed or not task["completed"]:
                status = "✔️" if task["completed"] else "❌"
                typer.echo(f"{i}. {status} {task['task']}")
@app.command()
def complete_task(task_number: int):
    """Mark a task as completed."""
    if 1 <= task_number <= len(tasks):
        tasks[task_number - 1]["completed"] = True
        typer.echo(f"Task {task_number} marked as completed.")
    else:
        typer.echo("Invalid task number. Please provide a valid task number.")
@app.command()
def delete_task(task_number: int):
    """Delete a task from the to-do list."""
    if 1 <= task_number <= len(tasks):
        deleted_task = tasks.pop(task_number - 1)
        typer.echo(f"Task '{deleted_task['task']}' deleted from the to-do list.")
    else:
        typer.echo("Invalid task number. Please provide a valid task number.")
if __name__ == "__main__":
    app()