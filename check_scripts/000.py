import requests as req
from utils import QuizFailedException
from utils import make_passed

if __name__ == '__main__':
    resp = req.get("http://localhost:8081/")
    status_code = resp.status_code
    message = resp.text

    if status_code != 200 or message != "Hello, world!":
        raise QuizFailedException('再仔细考虑一下呦~ 🤔')

    make_passed()
