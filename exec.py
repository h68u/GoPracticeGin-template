import os
import sys
from typing import Union

from check_scripts.quizexception import QuizFailedException

help_msg = '''
            #---*    [HELP]    *---#
    exec.py is a tool script helping execute commands.
It can be used to setup(actually rewrite) autograding
environment and check your exercises locally without
pushing your commits on GitHub.

Format:
    python exec [argument] [Optional]

Arguments:
    init [id]   --Init autograding environment.
                  Attention! You should always execute this first.

    test        --Check your quiz locally.

    help        --Show help messages.

    clean       --Clean up the files generated by command `test`

Anyway, you should read the README.md firstly. 😂
'''

action_template = """
name: GitHub Classroom Workflow

on: [push]

permissions:
  checks: write
  actions: read
  contents: read

jobs:
  build:
    name: Autograding
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - uses: actions/setup-go@v3.2.1
      with:
          go-version: 1.19

    - name: Collect Gependencies
      run: pip3 install requests
      
    - name: Build
      run: go build -o .checkspace/target  quizzes/quiz{:0>2d}/
      
    - name: Run after build
      run: ./.checkspace/target

    - uses: education/autograding@v1
"""

quiz_id: Union[int, str]


def update_autograding():
    classroom_yml = action_template.format(int(quiz_id))
    os.makedirs('.github/workflows/', exist_ok=True)
    with open('.github/workflows/classroom.yml', 'w+') as f:
        f.write(classroom_yml)

    os.system('git add .github/workflows/classroom.yml')
    os.system('git commit -m "Update Autograding"')
    os.system('git push')


def init_quiz_id():
    try:
        global quiz_id
        quiz_id = sys.argv[2]
    except:
        print('[ERROR] Missing quiz id.')
        exit(1)


def check_locally():
    init_quiz_id()
    os.makedirs('.checkspace/', exist_ok=True)
    os.system('go build -o .checkspace/target '
              'quizzes/quiz{:0>2d}/'.format(int(quiz_id)))
    os.system('./.checkspace/target')
    try:
        os.system('python check_scripts/{:0>2d}.py'
                  .format(quiz_id))
    except QuizFailedException as e:
        print(e)
        exit(1)

    exit(0)


def check():
    try:
        os.system('python check_scripts/{:0>2d}.py'
                  .format(quiz_id))
    except QuizFailedException as e:
        print(e)
        exit(1)

    exit(0)


def clean():
    try:
        os.removedirs('.checkspace')
    except Exception as e:
        print(e)
    finally:
        print('[INFO] All cleaned.')


def dispatch(arg):
    """dispatch

    Attention:
        All branches started with function call
        `init_quiz_id()`, need the extra argument : [id]
    """
    match arg:
        case 'init':
            init_quiz_id()
            update_autograding()

        case '__check':  # called by classroom action : education/autograding@v1
            init_quiz_id()
            check()

        case 'test':  # used for local test
            init_quiz_id()
            check_locally()

        case 'help':
            print(help_msg)

        case 'clean':
            clean()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[ERROR] Args were not enough.')
        exit(1)
    dispatch(sys.argv[1])
    exit(0)