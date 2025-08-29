from usecases.answer import AnswerUsecase


def get_answer_usecase() -> AnswerUsecase:
    """Get the answer usecase.

    Returns:
        The answer usecase.

    """
    return AnswerUsecase()
