
def make_passed():
    print('🥳🥰 PASSED! 🥳🥰')
    exit(0)


class QuizFailedException(Exception):
    """ QuizFailedException

    About:
        Should be raised when quiz failed.
    """

    def __init__(self, msg):
        self.msg = msg
