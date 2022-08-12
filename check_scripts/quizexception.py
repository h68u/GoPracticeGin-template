

class QuizFailedException(BaseException):
    """ QuizFailedException

    About:
        Should be raised when quiz failed.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
