# I will be frank why I made this. I wanted to use TASKS in two different functions/routes/decorators. I thought I could just go self.TASKS and wrap everything there in a class but then that felt complicated so I said 'nope' and well, we are here.

TASKS: dict[str, str] = {}

def clear_tasks():
    TASKS.clear()