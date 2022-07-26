import os
import shutil
import sys
import threading

from check_scripts.utils import QuizFailedException

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

    test [id]   --Check your quiz locally.

    help        --Show help messages.

    clean       --Clean up the files generated by command `test`

Anyway, you should read the README.md first. 😂
'''

action_template = '''
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

    - name: Collect Dependencies
      run: pip3 install requests
      
    - name: Build
      run: |
        mkdir -p .checkspace/ && \
        cd quizzes/quiz{:0>2d}/ && \
        go build -o target && \
        mv target ../../.checkspace/target
      
    - name: Run after build
      run: ./.checkspace/target

    - uses: education/autograding@v1
'''

quiz_id: int


def multithread_wrapper(task):
    """Run target in another thread."""
    p = threading.Thread(target=task)
    p.start()


def wake_target_win():
    def task_block():
        cmd_check_batch_win = '''\
        cd quizzes/quiz{:0>2d} && \
        go build -o target.exe && \
        mv target.exe ../../_checkspace/target.exe && \
        cd ../../_checkspace/ && \
        target.exe
        '''
        os.system(cmd_check_batch_win.format(quiz_id))
    multithread_wrapper(task_block)


def wake_target():
    def task_block():
        cmd_check_batch = '''\
        cd quizzes/quiz{:0>2d} && \
        go build -o target && \
        mv target.exe ../../_checkspace/target && \
        cd ../../_checkspace/ && \
        ./target
        '''
        os.system(cmd_check_batch.format(quiz_id))
    multithread_wrapper(task_block)


def update_autograding():
    classroom_yml = action_template.format(quiz_id)
    os.makedirs('.github/workflows/', exist_ok=True)
    with open('.github/workflows/classroom.yml', 'w+') as f:
        f.write(classroom_yml)

    os.system('git add .github/workflows/classroom.yml')
    os.system('git commit -m "Update Autograding"')
    os.system('git push')


def init_quiz_id():
    try:
        global quiz_id
        quiz_id = int(sys.argv[2])
    except:
        print('[ERROR] Missing quiz id.')
        exit(1)


def check_locally_win():
    os.makedirs('_checkspace/', exist_ok=True)
    wake_target_win()
    try:
        os.system('python check_scripts/{:0>3d}.py'
                  .format(quiz_id))
    except QuizFailedException as e:
        print(e.args[0])
        exit(1)


def check_locally():
    if sys.platform == 'win32':
        check_locally_win()
    else:
        os.makedirs('.checkspace/', exist_ok=True)
        wake_target()
        try:
            os.system('python check_scripts/{:0>3d}.py'
                      .format(quiz_id))
        except QuizFailedException as e:
            print(e)
            exit(1)

        exit(0)


def check():
    try:
        os.system('python check_scripts/{:0>3d}.py'
                  .format(quiz_id))
    except QuizFailedException as e:
        print(e)
        exit(1)

    exit(0)


def clean():
    try:
        shutil.rmtree('.checkspace')
    except Exception as e:
        print(e)
    try:
        shutil.rmtree('_checkspace')
    except Exception as e:
        print(e)
    print('[INFO] All cleaned.')


def dispatch(arg):
    """dispatch

    Attention:
        All branches started with function call
        `init_quiz_id()`, need the extra argument : [id]
    """
    if arg == 'init':
        init_quiz_id()
        update_autograding()

    elif arg == '__check':  # called by classroom action : education/autograding@v1
        init_quiz_id()
        check()

    elif arg == 'test':  # used for local test
        init_quiz_id()
        check_locally()

    elif arg == 'help':
        print(help_msg)

    elif arg == 'clean':
        clean()

    else:
        print('[ERROR] Unknown arg.')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[ERROR] Args were not enough.')
        exit(1)

    dispatch(sys.argv[1])
    exit(0)
