from usecases import TaskUsecase


def get_task_usecase() -> TaskUsecase:
    """Get the task usecase.

    Returns:
        The task usecase.

    """
    return TaskUsecase()
