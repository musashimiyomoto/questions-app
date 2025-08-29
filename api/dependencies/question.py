from usecases.question import QuestionUsecase


def get_question_usecase() -> QuestionUsecase:
    """Get the question usecase.

    Returns:
        The question usecase.

    """
    return QuestionUsecase()
